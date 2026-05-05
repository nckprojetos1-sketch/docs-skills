from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import sys
from dataclasses import dataclass
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
    headings: list[str]
    requirements: list[str]
    endpoints: list[str]
    acceptance: list[str]


@dataclass
class ExtractedDocument:
    source_pdf: Path
    metadata: dict[str, Any]
    page_count: int
    pages: list[PageContext]
    tables: list[dict[str, Any]]
    limitations: list[str]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "pdf-context"


def normalize_cell(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("\x00", " ")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[\t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_line(line: str) -> str:
    line = normalize_cell(line)
    line = re.sub(r"^[\-*•]\s+", "", line)
    return line.strip()


def unique_preserve(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        cleaned = normalize_line(item)
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
    return pdf_path.parent / f"{pdf_path.stem}-context"


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
    for raw in text.splitlines():
        line = normalize_line(raw)
        if not line or len(line) > 120:
            continue
        if re.match(r"^(\d+(\.\d+)*|[A-Z])[\).\- ]+\S", line):
            headings.append(line)
        elif line.endswith(":") and len(line.split()) <= 10:
            headings.append(line[:-1])
        elif line.isupper() and len(line.split()) <= 12:
            headings.append(line.title())
    return unique_preserve(headings)


REQ_ID_RE = re.compile(r"\b(?:RF|RNF|REQ|R|UC|CA|CR|AC)[-_ ]?\d{1,4}\b", re.IGNORECASE)
ENDPOINT_RE = re.compile(r"\b(?:GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(/[A-Za-z0-9_./{}:\-?=&%]+)", re.IGNORECASE)


def detect_requirement_lines(text: str) -> list[str]:
    lines: list[str] = []
    keywords = (
        "deve ",
        "devera ",
        "deverá ",
        "precisa ",
        "permitir ",
        "requisito",
        "funcional",
        "nao funcional",
        "não funcional",
        "obrigatorio",
        "obrigatório",
    )
    for raw in text.splitlines():
        line = normalize_line(raw)
        lower = line.lower()
        if REQ_ID_RE.search(line) or any(keyword in lower for keyword in keywords):
            if 8 <= len(line) <= 260:
                lines.append(line)
    return unique_preserve(lines)


def detect_endpoints(text: str) -> list[str]:
    endpoints = [match.group(0).upper().replace("  ", " ") for match in ENDPOINT_RE.finditer(text)]
    return unique_preserve(endpoints)


def detect_acceptance(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = normalize_line(raw)
        lower = line.lower()
        if any(term in lower for term in ("criterio de aceite", "critério de aceite", "aceite", "validar que", "dado que", "quando ", "entao ", "então ")):
            if 8 <= len(line) <= 260:
                lines.append(line)
    return unique_preserve(lines)


def detect_parameters_and_fields(text: str) -> list[str]:
    lines: list[str] = []
    field_re = re.compile(r"\b(?:campo|parametro|parâmetro|atributo|coluna|payload|body|query|string|number|boolean|integer|array|json)\b", re.IGNORECASE)
    for raw in text.splitlines():
        line = normalize_line(raw)
        if field_re.search(line) and 4 <= len(line) <= 260:
            lines.append(line)
    return unique_preserve(lines)


def detect_integrations(text: str) -> list[str]:
    lines: list[str] = []
    integration_re = re.compile(r"\b(?:api|sdk|webhook|oauth|jwt|token|servico|serviço|integracao|integração|endpoint|http|https://)\b", re.IGNORECASE)
    for raw in text.splitlines():
        line = normalize_line(raw)
        if integration_re.search(line) and 6 <= len(line) <= 260:
            lines.append(line)
    return unique_preserve(lines)


def classify_requirements(requirements: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    functional: list[str] = []
    nfr = {
        "UX": [],
        "Performance": [],
        "Seguranca": [],
        "Deploy": [],
        "Versionamento": [],
        "Observabilidade": [],
    }
    buckets = [
        ("UX", ("ux", "interface", "tela", "usuario", "usuário", "experiencia", "experiência", "usabilidade", "responsiv")),
        ("Performance", ("performance", "latencia", "latência", "tempo de resposta", "cache", "paginacao", "paginação", "limite")),
        ("Seguranca", ("seguranca", "segurança", "auth", "autentic", "autoriza", "token", "jwt", "oauth", "permiss")),
        ("Deploy", ("deploy", "ambiente", "infra", "hosped", "producao", "produção", "variavel", "variável")),
        ("Versionamento", ("versao", "versão", "version", "v1", "v2", "compatib", "breaking")),
        ("Observabilidade", ("log", "metric", "métrica", "monitor", "observab", "alerta", "erro")),
    ]
    for requirement in requirements:
        lower = requirement.lower()
        matched = False
        for bucket, keywords in buckets:
            if any(keyword in lower for keyword in keywords):
                nfr[bucket].append(requirement)
                matched = True
        if not matched:
            functional.append(requirement)
    return unique_preserve(functional), {key: unique_preserve(value) for key, value in nfr.items()}


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
    return normalize_cell(candidates[0][1])[:180] if candidates else ""


def table_to_records(page_number: int, table_index: int, raw_rows: list[list[Any]], title_or_context: str) -> dict[str, Any] | None:
    rows = [[normalize_cell(cell) for cell in row] for row in raw_rows]
    rows = [row for row in rows if any(cell for cell in row)]
    if len(rows) < 2:
        return None

    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    header = rows[0]
    if sum(1 for cell in header if cell) < 1:
        return None

    columns: list[str] = []
    seen: dict[str, int] = {}
    for idx, cell in enumerate(header):
        name = cell or f"coluna_{idx + 1}"
        count = seen.get(name.lower(), 0) + 1
        seen[name.lower()] = count
        columns.append(name if count == 1 else f"{name}_{count}")

    record_rows: list[dict[str, str]] = []
    for row in rows[1:]:
        record = {columns[idx]: row[idx] for idx in range(width)}
        if any(record.values()):
            record_rows.append(record)

    if not record_rows:
        return None

    return {
        "page": page_number,
        "table_index": table_index,
        "title_or_context": title_or_context or "Tabela extraida do PDF",
        "columns": columns,
        "rows": record_rows,
    }


def extract_with_fitz(pdf_path: Path) -> ExtractedDocument:
    if fitz is None:
        raise ExtractionError("PyMuPDF is not available.")

    doc = fitz.open(pdf_path)
    limitations: list[str] = []
    pages: list[PageContext] = []
    tables: list[dict[str, Any]] = []

    for page_idx in range(doc.page_count):
        page = doc.load_page(page_idx)
        text = normalize_text(page.get_text("text") or "")
        pages.append(
            PageContext(
                number=page_idx + 1,
                text=text,
                headings=detect_headings(text),
                requirements=detect_requirement_lines(text),
                endpoints=detect_endpoints(text),
                acceptance=detect_acceptance(text),
            )
        )

        if not hasattr(page, "find_tables"):
            continue
        try:
            finder = page.find_tables()
            page_tables = getattr(finder, "tables", []) or []
            blocks = page.get_text("blocks") or []
            for local_idx, table in enumerate(page_tables, start=1):
                raw_rows = table.extract()
                title = surrounding_context_from_blocks(blocks, getattr(table, "bbox", None))
                normalized = table_to_records(page_idx + 1, local_idx, raw_rows, title)
                if normalized:
                    tables.append(normalized)
        except Exception as exc:
            limitations.append(f"Table extraction failed on page {page_idx + 1}: {exc}")

    metadata = dict(doc.metadata or {})
    doc.close()
    return ExtractedDocument(pdf_path, metadata, len(pages), pages, tables, limitations)


def extract_with_pypdf(pdf_path: Path) -> ExtractedDocument:
    if PdfReader is None:
        raise ExtractionError("Neither PyMuPDF nor pypdf is available for PDF extraction.")
    reader = PdfReader(str(pdf_path))
    pages: list[PageContext] = []
    for page_idx, page in enumerate(reader.pages):
        text = normalize_text(page.extract_text() or "")
        pages.append(
            PageContext(
                number=page_idx + 1,
                text=text,
                headings=detect_headings(text),
                requirements=detect_requirement_lines(text),
                endpoints=detect_endpoints(text),
                acceptance=detect_acceptance(text),
            )
        )
    metadata = {str(k).strip("/"): str(v) for k, v in dict(reader.metadata or {}).items()}
    return ExtractedDocument(pdf_path, metadata, len(pages), pages, [], ["Used pypdf fallback; table extraction is unavailable."])


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


def compact(items: list[str], limit: int = 14) -> list[str]:
    return items[:limit]


def page_trace_line(page: PageContext) -> str:
    parts: list[str] = []
    if page.headings:
        parts.append("secoes: " + "; ".join(page.headings[:4]))
    if page.requirements:
        parts.append("requisitos: " + "; ".join(page.requirements[:3]))
    if page.endpoints:
        parts.append("endpoints: " + "; ".join(page.endpoints[:3]))
    if not parts:
        snippet = normalize_cell(page.text)[:180]
        parts.append(snippet if snippet else "sem texto extraivel")
    return f"- Pagina {page.number}: " + " | ".join(parts)


def find_section_lines(all_lines: list[str], keywords: tuple[str, ...], limit: int = 8) -> list[str]:
    matches: list[str] = []
    for line in all_lines:
        lower = line.lower()
        if any(keyword in lower for keyword in keywords):
            matches.append(line)
    return unique_preserve(matches)[:limit]


def infer_flows(requirements: list[str], endpoints: list[str]) -> list[str]:
    flows: list[str] = []
    for req in requirements:
        lower = req.lower()
        if any(term in lower for term in ("listar", "buscar", "consultar", "visualizar")):
            flows.append(f"Inferido: usuario consulta dados do sistema com base em requisito: {req}")
        elif any(term in lower for term in ("criar", "cadastrar", "adicionar")):
            flows.append(f"Inferido: usuario cadastra ou cria informacao com base em requisito: {req}")
        elif any(term in lower for term in ("editar", "atualizar", "alterar")):
            flows.append(f"Inferido: usuario atualiza informacao com base em requisito: {req}")
        elif any(term in lower for term in ("remover", "excluir", "deletar")):
            flows.append(f"Inferido: usuario remove informacao com base em requisito: {req}")
    for endpoint in endpoints:
        flows.append(f"Inferido: sistema consome endpoint `{endpoint}` conforme citado no PDF.")
    return unique_preserve(flows)[:10]


def render_list(items: list[str], empty: str) -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- {item}" for item in items)


def synthesize_readme(doc: ExtractedDocument, output_dir: Path) -> str:
    all_text = "\n".join(page.text for page in doc.pages)
    all_lines = unique_preserve([normalize_line(line) for line in all_text.splitlines() if normalize_line(line)])
    table_requirements: list[str] = []
    table_acceptance: list[str] = []
    table_fields: list[str] = []
    for table in doc.tables:
        for row in table["rows"]:
            row_lower = {key.lower(): value for key, value in row.items()}
            req_id = next((value for key, value in row_lower.items() if key in ("id", "codigo", "código")), "")
            req_text = next((value for key, value in row_lower.items() if "requisito" in key), "")
            acceptance_text = next((value for key, value in row_lower.items() if "aceite" in key or "criterio" in key or "critério" in key), "")
            if req_text:
                prefix = f"{req_id}: " if req_id else ""
                table_requirements.append(f"{prefix}{req_text}")
            if acceptance_text:
                prefix = f"{req_id}: " if req_id else ""
                table_acceptance.append(f"{prefix}{acceptance_text}")
            for key, value in row.items():
                if value and any(term in key.lower() for term in ("campo", "parametro", "parâmetro", "endpoint", "payload", "coluna")):
                    table_fields.append(f"{key}: {value}")
    all_requirements = unique_preserve([item for page in doc.pages for item in page.requirements] + table_requirements)
    req_ids = unique_preserve(REQ_ID_RE.findall(all_text))
    endpoints = unique_preserve([item for page in doc.pages for item in page.endpoints])
    acceptance = unique_preserve([item for page in doc.pages for item in page.acceptance] + table_acceptance)
    parameters = unique_preserve(detect_parameters_and_fields(all_text) + table_fields)
    integrations = detect_integrations(all_text)
    functional, nfr = classify_requirements(all_requirements)

    objective = find_section_lines(all_lines, ("objetivo", "proposito", "propósito", "finalidade"), 4)
    users = find_section_lines(all_lines, ("usuario", "usuário", "publico", "público", "persona", "ator"), 6)
    mvp = find_section_lines(all_lines, ("mvp", "escopo", "minimo", "mínimo", "deve conter"), 10)
    out_of_scope = find_section_lines(all_lines, ("fora de escopo", "nao inclui", "não inclui", "nao sera", "não será"), 6)
    risks = find_section_lines(all_lines, ("risco", "restricao", "restrição", "duvida", "dúvida", "pendencia", "pendência", "lacuna"), 10)
    explicit_flows = find_section_lines(all_lines, ("caso de uso", "fluxo", "jornada", "cenario", "cenário"), 10)
    flows = explicit_flows or infer_flows(functional, endpoints)

    title = doc.metadata.get("title") or doc.source_pdf.stem
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    sections: list[str] = [
        f"# Contexto PDF - {title}",
        "## Metadados do Documento Fonte",
        render_list(
            [
                f"Arquivo: `{doc.source_pdf.name}`",
                f"Caminho: `{doc.source_pdf}`",
                f"Paginas lidas: {doc.page_count}",
                f"Gerado em: {created_at}",
                f"Diretorio de saida: `{output_dir}`",
            ],
            "Metadados nao disponiveis.",
        ),
        "## Objetivo do Sistema",
        render_list(compact(objective, 6), "O PDF nao declara objetivo explicito; consultar rastreabilidade por pagina antes de planejar."),
        "## Publico e Usuarios",
        render_list(compact(users, 8), "O PDF nao declara publico ou usuarios explicitamente."),
        "## Escopo do MVP",
        render_list(compact(mvp, 12), "O PDF nao declara escopo de MVP explicitamente."),
        "## Fora de Escopo",
        render_list(compact(out_of_scope, 8), "Nenhum item fora de escopo foi identificado no PDF."),
        "## Requisitos Funcionais",
        render_list(compact(functional, 30), "Nenhum requisito funcional estruturado foi detectado automaticamente."),
        "## Requisitos Nao Funcionais",
    ]

    for bucket, values in nfr.items():
        sections.append(f"### {bucket}")
        sections.append(render_list(compact(values, 10), f"Nenhum requisito de {bucket.lower()} foi identificado."))

    sections.extend(
        [
            "## Endpoints, Parametros e Integracoes",
            "### Endpoints",
            render_list(compact(endpoints, 20), "Nenhum endpoint HTTP foi identificado."),
            "### Parametros e Campos",
            render_list(compact(parameters, 24), "Nenhum parametro ou campo importante foi identificado automaticamente."),
            "### Integracoes",
            render_list(compact(integrations, 20), "Nenhuma integracao foi identificada automaticamente."),
            "## Dados e Campos Importantes para Implementacao",
            render_list(compact(parameters, 24), "O PDF nao trouxe campos estruturados detectaveis fora das tabelas."),
            "## Casos de Uso e Fluxos",
            render_list(compact(flows, 14), "Nenhum caso de uso explicito ou fluxo inferivel foi identificado com base textual suficiente."),
            "## Criterios de Aceite",
            render_list(compact(acceptance, 20), "Nenhum criterio de aceite explicito foi identificado."),
            "## Tabelas Extraidas",
            render_list([f"Pagina {table['page']}, tabela {table['table_index']}: {table['title_or_context']} ({len(table['rows'])} linhas)" for table in doc.tables], "Nenhuma tabela real foi detectada; `tables.json` nao foi criado."),
            "## Riscos, Restricoes e Duvidas Abertas",
            render_list(compact(risks + doc.limitations, 14), "Nenhum risco, restricao, duvida aberta ou limitacao de extracao foi identificado."),
            "## Rastreabilidade por Pagina",
            "\n".join(page_trace_line(page) for page in doc.pages),
        ]
    )

    if req_ids:
        sections.extend(["## IDs de Requisito Detectados", render_list(req_ids, "Nenhum ID detectado.")])

    return "\n\n".join(sections).strip() + "\n"


def assert_readable_content(doc: ExtractedDocument) -> None:
    chars = sum(len(page.text) for page in doc.pages)
    readable_pages = sum(1 for page in doc.pages if len(page.text.strip()) >= 20)
    if doc.page_count == 0 or chars < 80 or readable_pages == 0:
        raise ExtractionError(
            "The PDF has no readable text. It may be scanned or image-only; OCR is outside docs-pdf-context v1."
        )


def run_checks(doc: ExtractedDocument, readme: str, wrote_tables: bool) -> list[str]:
    warnings: list[str] = []
    for page in doc.pages:
        if f"Pagina {page.number}:" not in readme:
            warnings.append(f"Missing traceability for page {page.number}.")
    for req_id in unique_preserve(REQ_ID_RE.findall("\n".join(page.text for page in doc.pages))):
        if req_id not in readme:
            warnings.append(f"Detected requirement ID not present in README: {req_id}")
    if doc.tables and not wrote_tables:
        warnings.append("Tables were detected but tables.json was not written.")
    if not doc.tables and wrote_tables:
        warnings.append("tables.json was written even though no table was detected.")
    if re.search(r"\b(?:TODO|PLACEHOLDER|\[TODO)\b", readme, re.IGNORECASE):
        warnings.append("README contains placeholder-like text.")
    return warnings


def write_outputs(doc: ExtractedDocument, output_dir: Path) -> dict[str, Any]:
    assert_readable_content(doc)
    output_dir.mkdir(parents=True, exist_ok=True)
    readme = synthesize_readme(doc, output_dir)
    readme_path = output_dir / "README.md"
    readme_path.write_text(readme, encoding="utf-8")

    tables_path: Path | None = None
    if doc.tables:
        tables_path = output_dir / "tables.json"
        tables_path.write_text(json.dumps({"tables": doc.tables}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        stale_tables = output_dir / "tables.json"
        if stale_tables.exists():
            stale_tables.unlink()

    warnings = run_checks(doc, readme, tables_path is not None)
    return {
        "valid": not warnings,
        "output_dir": str(output_dir),
        "readme": str(readme_path),
        "tables_json": str(tables_path) if tables_path else None,
        "page_count": doc.page_count,
        "tables_count": len(doc.tables),
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
