from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

DOCS_DIR_NAME = "DOCS-Engenharia-de-Contexto"
DOCS_REMOTE_URL = "https://github.com/nckprojetos1-sketch/DOCS-Engenharia-de-Contexto"

REQUIRED_DOCS_ENTRIES = [
    "README.md",
    "help",
    "references",
    "plans-to-be-executed",
    "plans-executed",
    "plans-abandoned",
]

REQUIRED_GENERATED_ENTRIES = [
    "context-registry-bootstrap.json",
    "context-registry.json",
    "context-registry-for-humans",
]


class ScriptError(RuntimeError):
    pass


def dump_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        raise ScriptError("Could not derive a slug from the provided value.")
    return slug


def resolve_repo_root(repo_path: str | None = None, cwd: str | None = None) -> Path:
    candidate = Path(repo_path or cwd or Path.cwd()).expanduser().resolve()

    if candidate.name == DOCS_DIR_NAME:
        return candidate.parent

    if (candidate / DOCS_DIR_NAME).is_dir():
        return candidate

    if repo_path is not None:
        return candidate

    for parent in [candidate, *candidate.parents]:
        if parent.name == DOCS_DIR_NAME:
            return parent.parent
        if (parent / DOCS_DIR_NAME).is_dir():
            return parent
        if (parent / ".git").exists():
            return parent

    return candidate


def validate_docs_root(docs_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not docs_root.is_dir():
        return [f"Missing DOCS root: {docs_root}"], warnings

    for entry in REQUIRED_DOCS_ENTRIES:
        if not (docs_root / entry).exists():
            errors.append(f"Missing required DOCS entry: {entry}")

    generated_root = docs_root / "references" / "_generated"
    if generated_root.exists():
        for entry in REQUIRED_GENERATED_ENTRIES:
            if not (generated_root / entry).exists():
                errors.append(f"Missing generated registry entry: references/_generated/{entry}")
    else:
        warnings.append("Missing references/_generated; bootstrap index validation skipped.")

    return errors, warnings


def write_file_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def unique_paths(paths: Iterable[Path]) -> list[Path]:
    seen: set[Path] = set()
    ordered: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            ordered.append(resolved)
    return ordered
