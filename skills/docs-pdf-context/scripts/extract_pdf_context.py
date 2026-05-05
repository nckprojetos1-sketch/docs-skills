from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DOCS_DIR_NAME = "DOCS-Engenharia-de-Contexto"

try:
    import fitz  # type: ignore
except Exception:  # pragma: no cover - depends on host environment
    fitz = None  # type: ignore

try:
    from pypdf import PdfReader  # type: ignore
except Exception:  # pragma: no cover - depends on host environment
    PdfReader = None  # type: ignore


class ExtractionError(RuntimeError):
    pass


@dataclass
class PageContext:
    number: int
    text: str
    headings: list[str] = field(default_factory=list)


@dataclass
class TableArtifact:
    table_id: str
    kind: str
    pages: list[int]
    source_table_indexes: list[int]
    title_or_context: str
    readme_anchor: str
    columns: list[str]
    rows: list[dict[str, Any]]


@dataclass
class ExtractedDocument:
    source_pdf: Path
    metadata: dict[str, Any]
    page_count: int
    pages: list[PageContext]
    tables: list[TableArtifact]
    callouts: list[dict[str, Any]]
    limitations: list[str]


SECTION_MARKERS = {
    "objective": "Objetivo do documento",
    "technical_base": "Base tecnica",
    "scope": "Escopo",
    "users": "Perfil usuario",
    "version": "Versao do documento",
    "date": "Data",
    "target_env": "Ambiente alvo",
    "executive_summary": "Resumo executivo",
}

ANCHORS_BY_KIND = {
    "api_resources": "api-endpoints-parametros-e-uso",
    "requirements": "requisitos-funcionais",
    "performance": "requisitos-nao-funcionais",
    "components": "arquitetura-minima-e-componentes",
    "delivery": "deploy-versionamento-e-entregaveis",
    "data_fields": "dados-e-campos-para-implementacao",
    "deliverables": "deploy-versionamento-e-entregaveis",
    "generic": "tabelas-estruturadas",
}

ID_PREFIX_BY_KIND = {
    "api_resources": "T-API",
    "requirements": "T-REQ",
    "performance": "T-PERF",
    "components": "T-COMP",
    "delivery": "T-DEL",
    "data_fields": "T-DATA",
    "deliverables": "T-OUT",
    "generic": "T-GEN",
}

REQ_ID_RE = re.compile(r"\b(?:RF|RNF|REQ|UC|CA|CR|AC)[-_ ]?\d{1,4}\b", re.IGNORECASE)
ENDPOINT_RE = re.compile(r"\b(?:GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(/[A-Za-z0-9_./{}:\-?=&%]+)", re.IGNORECASE)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", strip_accents(value).lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "pdf-context"


def strip_accents(value: str) -> str:
    replacements = str.maketrans(
        {
            "á": "a",
            "à": "a",
            "ã": "a",
            "â": "a",
            "ä": "a",
            "é": "e",
            "ê": "e",
            "í": "i",
            "ó": "o",
            "ô": "o",
            "õ": "o",
            "ú": "u",
            "ü": "u",
            "ç": "c",
            "Á": "A",
            "À": "A",
            "Ã": "A",
            "Â": "A",
            "É": "E",
            "Ê": "E",
            "Í": "I",
            "Ó": "O",
            "Ô": "O",
            "Õ": "O",
            "Ú": "U",
            "Ç": "C",
        }
    )
    return value.translate(replacements)


def normalize_cell(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("\x00", " ")
    text = text.replace("•", "-")
    text = re.sub(r"(?m)^\s*_+\s*$", "", text)
    text = re.sub(r"(?:\s+_+\s*)+", " ", text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = text.strip(" -\n\t")
    return fix_common_pdf_breaks(text)


def fix_common_pdf_breaks(text: str) -> str:
    replacements = {
        "best current price": "best_current_price",
        "stock quantity": "stock_quantity",
        "total stock": "total_stock",
        "stock lots": "stock_lots",
        "lot number": "lot_number",
        "tax profile": "tax_profile",
        "external ids": "external_ids",
        "valid from": "valid_from",
        "valid to": "valid_to",
        "unit price": "unit_price",
        "per page": "per_page",
        "is active": "is_active",
        "with stock": "with_stock",
        "with offers": "with_offers",
        "current price": "current_price",
    }
    for source, target in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        text = re.sub(rf"\b{re.escape(source)}\b", target, text, flags=re.IGNORECASE)
    text = re.sub(r"([A-Za-z0-9_/{},.;:])\n([a-z0-9_{])", r"\1 \2", text)
    text = re.sub(r"(?<!\w)_(?!\w)", " ", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = text.replace("•", "-")
    text = re.sub(r"[\t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def line_key(line: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", strip_accents(line).lower()).strip()


def clean_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in normalize_text(text).splitlines():
        line = normalize_cell(raw)
        if not line:
            continue
        if re.match(r"^\d+/\d+$", line):
            continue
        if line_key(line) in {"documento de requisitos minimos catalogo de produtos via api", "requisitos minimos catalogo de produtos via api", "mvp tecnico"}:
            continue
        lines.append(line)
    return lines


def unique_preserve(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        cleaned = normalize_cell(item)
        key = cleaned.lower()
        if cleaned and key not in seen:
            seen.add(key)
            result.append(cleaned)
    return result


def find_docs_root(start: Path) -> Path | None:
    candidates = [start, *start.parents, Path.cwd(), *Path.cwd().parents]
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.name == DOCS_DIR_NAME and resolved.is_dir():
            return resolved
        docs_root = resolved / DOCS_DIR_NAME
        if docs_root.is_dir():
            return docs_root
    return None


def resolve_output_dir(pdf_path: Path, explicit_out: str | None) -> Path:
    if explicit_out:
        return Path(explicit_out).expanduser().resolve()
    docs_root = find_docs_root(pdf_path.parent)
    if docs_root:
        return docs_root / "references" / "global" / slugify(pdf_path.stem)
    return pdf_path.parent / f"{slugify(pdf_path.stem)}"


def validate_pdf(path_value: str) -> Path:
    path = Path(path_value).expanduser().resolve()
    if not path.exists():
        raise ExtractionError(f"PDF not found: {path}")
    if not path.is_file():
        raise ExtractionError(f"PDF path is not a file: {path}")
    if path.suffix.lower() != ".pdf":
        raise ExtractionError(f"Expected a .pdf file, got: {path}")
    return path


def detect_headings(text: str) -> list[str]:
    headings: list[str] = []
    for line in clean_lines(text):
        key = line_key(line)
        if key in {line_key(value) for value in SECTION_MARKERS.values()}:
            headings.append(line)
            continue
        if re.match(r"^\d+(\.\d+)*\.\s+\S", line) or re.match(r"^\d+(\.\d+)*\s+-?\s*[A-Za-z]", line):
            headings.append(line)
            continue
        if len(line) <= 90 and any(term in key for term in ("escopo minimo", "requisitos funcionais", "requisitos de ux", "requisitos de performance", "requisitos de seguranca", "tratamento de dados", "criterios de aceite", "entregaveis minimos")):
            headings.append(line)
    return unique_preserve(headings)


def classify_table(columns: list[str]) -> str:
    normalized = [line_key(column) for column in columns]
    joined = " | ".join(normalized)
    if "id" in normalized and "requisito" in joined and "aceite" in joined:
        return "requirements"
    if "recurso" in joined and "endpoint" in joined:
        return "api_resources"
    if "area" in normalized and "meta recomendada" in joined:
        return "performance"
    if "componente" in joined and "responsabilidade" in joined:
        return "components"
    if "grupo" in normalized and "campos minimos" in joined:
        return "data_fields"
    if "entregavel" in joined and "descricao" in joined:
        return "deliverables"
    if "item" in normalized and "criterio de aceite" in joined:
        return "delivery"
    return "generic"


def is_real_table(rows: list[list[str]]) -> bool:
    if len(rows) < 2:
        return False
    header = rows[0]
    non_empty_header = [cell for cell in header if cell]
    if len(non_empty_header) < 2:
        return False
    body_rows = [row for row in rows[1:] if sum(1 for cell in row if cell) >= 2]
    if not body_rows:
        return False
    return True


def normalize_rows(raw_rows: list[list[Any]]) -> list[list[str]]:
    rows = [[normalize_cell(cell) for cell in row] for row in raw_rows]
    rows = [row for row in rows if any(cell for cell in row)]
    if not rows:
        return []
    width = max(len(row) for row in rows)
    return [row + [""] * (width - len(row)) for row in rows]


def extract_callout_from_rows(page_number: int, table_index: int, rows: list[list[str]], context: str) -> dict[str, Any] | None:
    text_parts: list[str] = []
    for row in rows:
        for cell in row:
            if cell:
                text_parts.append(cell)
    text = normalize_cell("\n".join(text_parts))
    if not text:
        return None
    return {
        "callout_id": f"C-P{page_number:02d}-{table_index:02d}",
        "page": page_number,
        "source_table_index": table_index,
        "title_or_context": context,
        "text": text,
    }


def table_from_rows(page_number: int, table_index: int, rows: list[list[str]], context: str) -> TableArtifact | None:
    if not is_real_table(rows):
        return None
    columns = rows[0]
    kind = classify_table(columns)
    seen_columns: dict[str, int] = {}
    stable_columns: list[str] = []
    for idx, column in enumerate(columns):
        name = column or f"coluna_{idx + 1}"
        count = seen_columns.get(name.lower(), 0) + 1
        seen_columns[name.lower()] = count
        stable_columns.append(name if count == 1 else f"{name}_{count}")

    return TableArtifact(
        table_id="",
        kind=kind,
        pages=[page_number],
        source_table_indexes=[table_index],
        title_or_context=context or infer_table_title(kind),
        readme_anchor=ANCHORS_BY_KIND.get(kind, ANCHORS_BY_KIND["generic"]),
        columns=stable_columns,
        rows=[
            {
                "row_id": "",
                "source_pages": [page_number],
                "readme_refs": [],
                "cells": {stable_columns[idx]: row[idx] for idx in range(len(stable_columns))},
            }
            for row in rows[1:]
            if any(row)
        ],
    )


def infer_table_title(kind: str) -> str:
    return {
        "api_resources": "Recursos e parametros da API",
        "requirements": "Requisitos funcionais e criterios de aceite",
        "performance": "Requisitos de performance",
        "components": "Componentes minimos",
        "delivery": "Requisitos de Docker, versionamento e entrega",
        "data_fields": "Campos minimos exibidos",
        "deliverables": "Entregaveis minimos esperados",
    }.get(kind, "Tabela estruturada extraida do PDF")


def table_signature(table: TableArtifact) -> tuple[str, tuple[str, ...]]:
    return table.kind, tuple(line_key(column) for column in table.columns)


def merge_related_tables(tables: list[TableArtifact]) -> list[TableArtifact]:
    merged: list[TableArtifact] = []
    for table in tables:
        if merged and table_signature(merged[-1]) == table_signature(table) and table.pages[0] <= merged[-1].pages[-1] + 1:
            current = merged[-1]
            current.pages = unique_ints(current.pages + table.pages)
            current.source_table_indexes.extend(table.source_table_indexes)
            current.rows.extend(table.rows)
            if table.title_or_context and table.title_or_context not in current.title_or_context:
                current.title_or_context = current.title_or_context or table.title_or_context
            continue
        merged.append(table)
    assign_table_ids(merged)
    return merged


def assign_table_ids(tables: list[TableArtifact]) -> None:
    counters: dict[str, int] = {}
    for table in tables:
        prefix = ID_PREFIX_BY_KIND.get(table.kind, ID_PREFIX_BY_KIND["generic"])
        counters[prefix] = counters.get(prefix, 0) + 1
        table.table_id = f"{prefix}-{counters[prefix]:03d}"
        for index, row in enumerate(table.rows, start=1):
            req_id = get_cell(row, "id")
            row["row_id"] = req_id if req_id else f"{table.table_id}-R{index:03d}"
            row["readme_refs"] = [table.readme_anchor]


def unique_ints(values: list[int]) -> list[int]:
    seen: set[int] = set()
    result: list[int] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def get_cell(row: dict[str, Any], contains: str) -> str:
    cells = row.get("cells", row)
    for key, value in cells.items():
        if key_matches(str(key), contains):
            return normalize_cell(value)
    return ""


def key_matches(key: str, contains: str | None) -> bool:
    if not contains:
        return False
    key_tokens = line_key(key).split()
    contains_tokens = line_key(contains).split()
    if not contains_tokens:
        return False
    if contains_tokens == key_tokens:
        return True
    if len(contains_tokens) == 1:
        return contains_tokens[0] in key_tokens
    joined_key = " ".join(key_tokens)
    joined_contains = " ".join(contains_tokens)
    return joined_contains in joined_key


def surrounding_context_from_blocks(blocks: list[Any], bbox: Any) -> str:
    try:
        top = float(bbox[1])
    except Exception:
        return ""
    candidates: list[tuple[float, str]] = []
    for block in blocks:
        if len(block) < 5:
            continue
        text = normalize_cell(block[4])
        if not text:
            continue
        try:
            bottom = float(block[3])
        except Exception:
            continue
        if bottom <= top:
            candidates.append((top - bottom, text))
    candidates.sort(key=lambda item: item[0])
    return normalize_cell(candidates[0][1])[:220] if candidates else ""


def extract_with_fitz(pdf_path: Path) -> ExtractedDocument:
    if fitz is None:
        raise ExtractionError("PyMuPDF is not available.")

    doc = fitz.open(pdf_path)
    limitations: list[str] = []
    pages: list[PageContext] = []
    raw_tables: list[TableArtifact] = []
    callouts: list[dict[str, Any]] = []

    for page_idx in range(doc.page_count):
        page_number = page_idx + 1
        page = doc.load_page(page_idx)
        text = normalize_text(page.get_text("text") or "")
        pages.append(PageContext(number=page_number, text=text, headings=detect_headings(text)))

        if not hasattr(page, "find_tables"):
            continue
        try:
            finder = page.find_tables()
            page_tables = getattr(finder, "tables", []) or []
            blocks = page.get_text("blocks") or []
            for local_idx, table in enumerate(page_tables, start=1):
                rows = normalize_rows(table.extract())
                context = surrounding_context_from_blocks(blocks, getattr(table, "bbox", None))
                artifact = table_from_rows(page_number, local_idx, rows, context)
                if artifact:
                    raw_tables.append(artifact)
                    continue
                callout = extract_callout_from_rows(page_number, local_idx, rows, context)
                if callout:
                    callouts.append(callout)
        except Exception as exc:
            limitations.append(f"Table extraction failed on page {page_number}: {exc}")

    metadata = dict(doc.metadata or {})
    doc.close()
    return ExtractedDocument(pdf_path, metadata, len(pages), pages, merge_related_tables(raw_tables), callouts, limitations)


def extract_with_pypdf(pdf_path: Path) -> ExtractedDocument:
    if PdfReader is None:
        raise ExtractionError("Neither PyMuPDF nor pypdf is available for PDF extraction.")
    reader = PdfReader(str(pdf_path))
    pages: list[PageContext] = []
    for page_idx, page in enumerate(reader.pages):
        text = normalize_text(page.extract_text() or "")
        pages.append(PageContext(number=page_idx + 1, text=text, headings=detect_headings(text)))
    metadata = {str(k).strip("/"): str(v) for k, v in dict(reader.metadata or {}).items()}
    return ExtractedDocument(pdf_path, metadata, len(pages), pages, [], [], ["Used pypdf fallback; table extraction is unavailable."])


def extract_document(pdf_path: Path) -> ExtractedDocument:
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return extract_with_fitz(pdf_path)
    except Exception as fitz_exc:
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                doc = extract_with_pypdf(pdf_path)
            doc.limitations.insert(0, f"PyMuPDF extraction failed: {fitz_exc}")
            return doc
        except Exception as pypdf_exc:
            raise ExtractionError(f"Could not extract PDF text. PyMuPDF error: {fitz_exc}; pypdf error: {pypdf_exc}") from pypdf_exc


def assert_readable_content(doc: ExtractedDocument) -> None:
    chars = sum(len(page.text) for page in doc.pages)
    readable_pages = sum(1 for page in doc.pages if len(page.text.strip()) >= 20)
    if doc.page_count == 0 or chars < 80 or readable_pages == 0:
        raise ExtractionError(
            "The PDF has no readable text. It may be scanned or image-only; OCR is outside docs-pdf-context v1."
        )


def all_lines_by_page(doc: ExtractedDocument) -> dict[int, list[str]]:
    return {page.number: clean_lines(page.text) for page in doc.pages}


def flattened_lines(doc: ExtractedDocument) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for page in doc.pages:
        result.extend((page.number, line) for line in clean_lines(page.text))
    return result


def extract_label_values(doc: ExtractedDocument) -> dict[str, dict[str, Any]]:
    lines = flattened_lines(doc)
    marker_keys = {line_key(value): name for name, value in SECTION_MARKERS.items()}
    values: dict[str, dict[str, Any]] = {}
    index = 0
    while index < len(lines):
        page, line = lines[index]
        key = marker_keys.get(line_key(line))
        if not key:
            index += 1
            continue
        collected: list[str] = []
        index += 1
        while index < len(lines):
            next_page, next_line = lines[index]
            if line_key(next_line) in marker_keys or re.match(r"^\d+\.\s+", next_line):
                break
            collected.append(next_line)
            index += 1
        values[key] = {"text": normalize_cell(" ".join(collected)), "page": page}
    return values


def capture_bullets(doc: ExtractedDocument, start_markers: tuple[str, ...], stop_markers: tuple[str, ...]) -> list[dict[str, Any]]:
    lines = flattened_lines(doc)
    collecting = False
    raw_items: list[dict[str, Any]] = []
    for page, line in lines:
        key = line_key(line)
        if not collecting and any(marker in key for marker in start_markers):
            collecting = True
            continue
        if collecting and any(marker in key for marker in stop_markers):
            break
        if not collecting:
            continue
        if line == "-":
            continue
        if line.startswith("- "):
            line = line[2:]
        if len(line) > 3:
            raw_items.append({"text": line, "page": page})
    return merge_continuation_items(raw_items)


def merge_continuation_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for item in items:
        text = item["text"]
        if merged and should_merge_continuation(merged[-1]["text"], text):
            merged[-1]["text"] = normalize_cell(f"{merged[-1]['text']} {text}")
            continue
        merged.append(dict(item))
    return merged


def should_merge_continuation(previous: str, current: str) -> bool:
    if not previous or not current:
        return False
    if previous.endswith((".", ";", ":", "?", "!")):
        return False
    first = current[:1]
    if first.islower():
        return True
    previous_key = line_key(previous)
    return previous_key.endswith((" de", " da", " do", " das", " dos", " nos", " nas", " e", " com", " para"))


def find_table(doc: ExtractedDocument, kind: str) -> TableArtifact | None:
    return next((table for table in doc.tables if table.kind == kind), None)


def find_tables(doc: ExtractedDocument, kind: str) -> list[TableArtifact]:
    return [table for table in doc.tables if table.kind == kind]


def row_ref(table: TableArtifact, row: dict[str, Any]) -> str:
    pages = ", ".join(f"p.{page}" for page in row.get("source_pages", table.pages))
    return f"{pages}; {table.table_id}/{row['row_id']}"


def table_ref(table: TableArtifact) -> str:
    pages = ", ".join(f"p.{page}" for page in table.pages)
    return f"{pages}; {table.table_id}"


def list_text(items: list[dict[str, Any]], limit: int | None = None) -> list[str]:
    values = [item["text"] for item in items]
    return unique_preserve(values[:limit] if limit else values)


def render_bullets(items: list[str], empty: str = "Nao identificado no PDF.") -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- {item}" for item in items)


def render_requirement_table(table: TableArtifact | None) -> str:
    if not table:
        return "- Nenhuma tabela de requisitos funcionais foi detectada."
    lines = []
    for row in table.rows:
        req_id = get_cell(row, "id") or row["row_id"]
        requirement = get_cell(row, "requisito")
        acceptance = get_cell(row, "aceite") or get_cell(row, "criterio")
        lines.append(f"- `{req_id}` - {requirement} Aceite: {acceptance} Fonte: {row_ref(table, row)}.")
    return "\n".join(lines)


def render_api_resources(table: TableArtifact | None) -> str:
    if not table:
        return "- Nenhum recurso de API estruturado foi detectado."
    lines = []
    for row in table.rows:
        resource = get_cell(row, "recurso")
        endpoint = get_cell(row, "endpoint") or get_cell(row, "parametro")
        usage = get_cell(row, "uso")
        lines.append(f"- `{endpoint}` - {resource}: {usage} Fonte: {row_ref(table, row)}.")
    return "\n".join(lines)


def render_performance(table: TableArtifact | None) -> str:
    if not table:
        return "- Nenhuma tabela de performance foi detectada."
    lines = []
    for row in table.rows:
        area = get_cell(row, "area")
        requirement = get_cell(row, "requisito")
        target = get_cell(row, "meta")
        lines.append(f"- {area}: {requirement} Meta: {target} Fonte: {row_ref(table, row)}.")
    return "\n".join(lines)


def render_simple_table_rows(table: TableArtifact | None, first_key: str, second_key: str, third_key: str | None = None) -> str:
    if not table:
        return "- Nao identificado no PDF."
    lines = []
    for row in table.rows:
        first = get_cell(row, first_key)
        second = get_cell(row, second_key)
        third = get_cell(row, third_key) if third_key else ""
        suffix = f" {third}" if third else ""
        lines.append(f"- {first}: {second}{suffix} Fonte: {row_ref(table, row)}.")
    return "\n".join(lines)


def render_components(table: TableArtifact | None) -> str:
    if not table:
        return "- Nao identificado no PDF."
    lines = []
    for row in table.rows:
        component = get_cell(row, "componente")
        required = get_cell(row, "obrigatorio")
        responsibility = get_cell(row, "responsabilidade")
        lines.append(f"- {component} ({required}): {responsibility} Fonte: {row_ref(table, row)}.")
    return "\n".join(lines)


def render_data_fields(table: TableArtifact | None) -> str:
    if not table:
        return "- Nao identificado no PDF."
    lines = []
    for row in table.rows:
        group = get_cell(row, "grupo")
        fields = get_cell(row, "campos")
        observation = get_cell(row, "observacao")
        lines.append(f"- {group}: {fields}. Observacao: {observation} Fonte: {row_ref(table, row)}.")
    return "\n".join(lines)


def render_traceability(doc: ExtractedDocument) -> str:
    lines = []
    tables_by_page: dict[int, list[str]] = {}
    for table in doc.tables:
        for page in table.pages:
            tables_by_page.setdefault(page, []).append(table.table_id)
    callouts_by_page: dict[int, list[str]] = {}
    for callout in doc.callouts:
        callouts_by_page.setdefault(callout["page"], []).append(callout["callout_id"])
    for page in doc.pages:
        headings = "; ".join(page.headings[:5]) if page.headings else "sem headings confiaveis"
        table_ids = ", ".join(tables_by_page.get(page.number, [])) or "sem tabelas reais"
        callout_ids = ", ".join(callouts_by_page.get(page.number, [])) or "sem callouts"
        lines.append(f"- Pagina {page.number}: {headings}. Tabelas: {table_ids}. Callouts: {callout_ids}.")
    return "\n".join(lines)


def render_tables_index(doc: ExtractedDocument) -> str:
    if not doc.tables:
        return "- Nenhuma tabela real foi detectada; `tables.json` nao foi criado."
    return "\n".join(f"- `{table.table_id}` ({table.kind}, {table_ref(table)}): {table.title_or_context}; {len(table.rows)} linhas." for table in doc.tables)


def render_callouts(doc: ExtractedDocument) -> str:
    if not doc.callouts:
        return "- Nenhum callout narrativo separado das tabelas foi detectado."
    return "\n".join(f"- `{callout['callout_id']}` (p.{callout['page']}): {callout['text']}" for callout in doc.callouts)


def synthesize_readme(doc: ExtractedDocument, output_dir: Path) -> str:
    labels = extract_label_values(doc)
    api_table = find_table(doc, "api_resources")
    requirements_table = find_table(doc, "requirements")
    performance_table = find_table(doc, "performance")
    components_table = find_table(doc, "components")
    data_fields_table = find_table(doc, "data_fields")
    deliverables_table = find_table(doc, "deliverables")
    delivery_tables = find_tables(doc, "delivery")

    mvp_in = capture_bullets(doc, ("o que entra no mvp",), ("o que fica fora do mvp", "2 base tecnica"))
    mvp_out = capture_bullets(doc, ("o que fica fora do mvp",), ("2 base tecnica",))
    ux_items = capture_bullets(doc, ("requisitos minimos de interface",), ("5 requisitos de performance",))
    stack_items = capture_bullets(doc, ("stack minima sugerida",), ("exemplo minimo de variaveis", "7 requisitos de docker"))
    security_items = capture_bullets(doc, ("8 requisitos de seguranca",), ("9 tratamento de dados",))
    acceptance_items = capture_bullets(doc, ("10 criterios de aceite",), ("11 entregaveis minimos",))

    title = doc.metadata.get("title") or "Requisitos Minimos - Catalogo de Produtos via API"
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    delivery_sections: list[str] = []
    for table in delivery_tables:
        delivery_sections.append(render_simple_table_rows(table, "item", "requisito", "aceite"))

    lines = [
        f"# Contexto Operacional - {title}",
        "## Metadados",
        render_bullets(
            [
                f"Arquivo fonte: `{doc.source_pdf.name}`.",
                f"Caminho fonte: `{doc.source_pdf}`.",
                f"Paginas lidas: {doc.page_count}.",
                f"Pacote gerado em: {created_at}.",
                f"Diretorio de saida: `{output_dir}`.",
                "Uso esperado: contexto autossuficiente para abrir AP ou SDDR depois, sem promover plano automaticamente.",
            ]
        ),
        "## Visao Executiva",
        render_bullets(
            [
                f"Objetivo: {labels.get('objective', {}).get('text', 'Nao identificado no PDF.')}",
                f"Resumo: {labels.get('executive_summary', {}).get('text', 'Nao identificado no PDF.')}",
                f"Publico usuario: {labels.get('users', {}).get('text', 'Nao identificado no PDF.')}",
                f"Ambiente alvo: {labels.get('target_env', {}).get('text', 'Nao identificado no PDF.')}",
                f"Base tecnica citada: {labels.get('technical_base', {}).get('text', 'Nao identificada no PDF.')}",
            ]
        ),
        "## Escopo do MVP",
        "### Entra no MVP",
        render_bullets([f"{item['text']} Fonte: p.{item['page']}." for item in mvp_in]),
        "### Fora do MVP",
        render_bullets([f"{item['text']} Fonte: p.{item['page']}." for item in mvp_out]),
        "## API, Endpoints, Parametros e Uso",
        render_api_resources(api_table),
        "## Requisitos Funcionais",
        render_requirement_table(requirements_table),
        "## Requisitos Nao Funcionais",
        "### UX",
        render_bullets([f"{item['text']} Fonte: p.{item['page']}." for item in ux_items]),
        "### Performance",
        render_performance(performance_table),
        "### Seguranca",
        render_bullets([f"{item['text']} Fonte: p.{item['page']}." for item in security_items]),
        "### Deploy, Versionamento e Entrega",
        "\n".join(delivery_sections) if delivery_sections else "- Nao identificado no PDF.",
        "## Arquitetura Minima e Componentes",
        "### Componentes",
        render_components(components_table),
        "### Stack e Configuracao",
        render_bullets([f"{item['text']} Fonte: p.{item['page']}." for item in stack_items]),
        "## Dados e Campos Para Implementacao",
        render_data_fields(data_fields_table),
        "## Fluxos De Uso",
        render_bullets(infer_flows(requirements_table, api_table)),
        "## Criterios De Aceite Do MVP",
        render_bullets([f"{item['text']} Fonte: p.{item['page']}." for item in acceptance_items]),
        "## Entregaveis Esperados",
        render_simple_table_rows(deliverables_table, "entregavel", "descricao"),
        "## Callouts E Decisoes Narrativas",
        render_callouts(doc),
        "## Indice De Tabelas Estruturadas",
        render_tables_index(doc),
        "## Rastreabilidade Por Pagina",
        render_traceability(doc),
    ]

    if doc.limitations:
        lines.extend(["## Limitacoes De Extracao", render_bullets(doc.limitations)])

    return "\n\n".join(lines).strip() + "\n"


def infer_flows(requirements_table: TableArtifact | None, api_table: TableArtifact | None) -> list[str]:
    flows: list[str] = []
    if requirements_table:
        for row in requirements_table.rows:
            req_id = get_cell(row, "id") or row["row_id"]
            requirement = get_cell(row, "requisito")
            lower = line_key(requirement)
            if "listar" in lower:
                flows.append(f"Inferido: vendedor abre o catalogo e visualiza produtos em card ou tabela. Base: {row_ref(requirements_table, row)}.")
            elif "buscar" in lower:
                flows.append(f"Inferido: vendedor digita uma busca, a aplicacao chama a API com `search` e atualiza a lista sem recarregar a pagina. Base: {row_ref(requirements_table, row)}.")
            elif "filtrar" in lower:
                flows.append(f"Inferido: vendedor combina filtros de categoria, marca e status para restringir resultados. Base: {row_ref(requirements_table, row)}.")
            elif "detalhe" in lower:
                flows.append(f"Inferido: vendedor abre um produto e consulta dados completos sem perder o contexto da listagem. Base: {row_ref(requirements_table, row)}.")
            elif "copiar" in lower:
                flows.append(f"Inferido: vendedor copia informacoes comerciais para uso em atendimento ou venda. Base: {row_ref(requirements_table, row)}.")
            elif req_id:
                continue
    if api_table:
        endpoints = [get_cell(row, "endpoint") or get_cell(row, "parametro") for row in api_table.rows]
        if any("/v2/products/card" in endpoint for endpoint in endpoints):
            flows.append(f"Inferido: listagens devem preferir dados resumidos de `/v2/products/card` quando disponivel. Base: {table_ref(api_table)}.")
    return unique_preserve(flows)


def table_to_json(table: TableArtifact) -> dict[str, Any]:
    return {
        "table_id": table.table_id,
        "kind": table.kind,
        "pages": table.pages,
        "source_table_indexes": table.source_table_indexes,
        "title_or_context": table.title_or_context,
        "readme_anchor": table.readme_anchor,
        "columns": table.columns,
        "rows": table.rows,
    }


def build_context_json(doc: ExtractedDocument, output_dir: Path) -> dict[str, Any]:
    return {
        "source": {
            "pdf": str(doc.source_pdf),
            "metadata": doc.metadata,
            "page_count": doc.page_count,
            "output_dir": str(output_dir),
        },
        "pages": [
            {
                "page": page.number,
                "headings": page.headings,
                "text": "\n".join(clean_lines(page.text)),
            }
            for page in doc.pages
        ],
        "callouts": doc.callouts,
        "tables": [table_to_json(table) for table in doc.tables],
        "limitations": doc.limitations,
    }


def run_checks(doc: ExtractedDocument, readme: str, wrote_tables: bool) -> list[str]:
    warnings: list[str] = []
    all_text = "\n".join(page.text for page in doc.pages)
    for page in doc.pages:
        if f"Pagina {page.number}:" not in readme:
            warnings.append(f"Missing traceability for page {page.number}.")
    for req_id in unique_preserve([match.upper().replace(" ", "-").replace("_", "-") for match in REQ_ID_RE.findall(all_text)]):
        if req_id not in readme:
            warnings.append(f"Detected requirement ID not present in README: {req_id}")
    for table in doc.tables:
        if table.table_id not in readme:
            warnings.append(f"Detected table not referenced in README: {table.table_id}")
    if doc.tables and not wrote_tables:
        warnings.append("Tables were detected but tables.json was not written.")
    if not doc.tables and wrote_tables:
        warnings.append("tables.json was written even though no table was detected.")
    if re.search(r"\b(?:TODO|PLACEHOLDER|\[TODO)\b", readme, re.IGNORECASE):
        warnings.append("README contains placeholder-like text.")
    if "_ _" in readme:
        warnings.append("README contains raw PDF underscore artifacts.")
    return warnings


def write_outputs(doc: ExtractedDocument, output_dir: Path) -> dict[str, Any]:
    assert_readable_content(doc)
    output_dir.mkdir(parents=True, exist_ok=True)

    context_path = output_dir / "context.json"
    context_path.write_text(json.dumps(build_context_json(doc, output_dir), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    readme = synthesize_readme(doc, output_dir)
    readme_path = output_dir / "README.md"
    readme_path.write_text(readme, encoding="utf-8")

    tables_path: Path | None = None
    if doc.tables:
        tables_path = output_dir / "tables.json"
        tables_path.write_text(json.dumps({"tables": [table_to_json(table) for table in doc.tables]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        stale_tables = output_dir / "tables.json"
        if stale_tables.exists():
            stale_tables.unlink()

    warnings = run_checks(doc, readme, tables_path is not None)
    return {
        "valid": not warnings,
        "output_dir": str(output_dir),
        "readme": str(readme_path),
        "context_json": str(context_path),
        "tables_json": str(tables_path) if tables_path else None,
        "page_count": doc.page_count,
        "tables_count": len(doc.tables),
        "callouts_count": len(doc.callouts),
        "limitations": doc.limitations,
        "warnings": warnings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract a requirements PDF into a DOCS context package.")
    parser.add_argument("pdf", help="Path to the requirements PDF.")
    parser.add_argument("--out", help="Output directory. When omitted, DOCS references/global or <pdf-stem>-context is used.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        pdf_path = validate_pdf(args.pdf)
        output_dir = resolve_output_dir(pdf_path, args.out)
        doc = extract_document(pdf_path)
        payload = write_outputs(doc, output_dir)
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if payload["valid"] else 2
    except ExtractionError as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
