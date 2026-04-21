from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from common import DOCS_DIR_NAME, DOCS_REMOTE_URL, ScriptError, dump_json, resolve_repo_root, validate_docs_root, write_file_if_missing


README = """# DOCS - Engenharia de Contexto

Documentacao oficial do metodo.

DOCS e um metodo de engenharia de contexto para trabalho orientado por IA.

Estrutura oficial:

- help/
- references/
- plans-to-be-executed/
- plans-executed/
- plans-abandoned/

Hierarquia de verdade:

1. codigo vivo do repositorio
2. planos e subplanos relevantes
3. references/ como indice e apoio global
4. historico restante
"""

BOOTSTRAP_CORE = """# bootstrap-core

Leitura central do metodo DOCS.

## Verdade do sistema

1. codigo vivo do repositorio
2. plano, subplano ou etapa relevante
3. references/ como indice e apoio global
4. historico restante

## Fluxo oficial de descoberta

1. abrir references/README.md
2. abrir references/_generated/context-registry-bootstrap.json
3. localizar o tema
4. abrir best_entry_path
5. abrir context-registry.json somente se faltarem sinais
6. abrir context-registry-for-humans/<bucket>.md somente se a busca ainda estiver ampla
7. abrir codigo correlato
"""

CONVENTIONS = """# conventions

Regras canonicas do metodo DOCS.

- Todo plano fica em plans-to-be-executed/, plans-executed/ ou plans-abandoned/.
- AP usa subplanos NN-name__sp com 01-sddd/.
- SDDR nao usa xx-sddd.
- Estados oficiais: draft, ready, running, blocked, completed.
- Handoff fica em reports/ ou na resposta final, nunca em agent-audit/.
"""


def normalize_docs(docs_root: Path) -> list[str]:
    created: list[str] = []

    directories = [
        docs_root / "help" / "inits" / "init-agents",
        docs_root / "help" / "templates",
        docs_root / "references" / "global",
        docs_root / "references" / "history",
        docs_root / "references" / "_generated" / "agent-audit",
        docs_root / "references" / "_generated" / "context-registry-for-humans",
        docs_root / "plans-to-be-executed",
        docs_root / "plans-executed",
        docs_root / "plans-abandoned",
    ]
    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            created.append(str(directory))

    files = {
        docs_root / "README.md": README,
        docs_root / "help" / "bootstrap-core.md": BOOTSTRAP_CORE,
        docs_root / "help" / "conventions.md": CONVENTIONS,
        docs_root / "help" / "README.md": "# help\n\nCamada normativa do DOCS.\n",
        docs_root / "references" / "README.md": "# references\n\nIndice e apoio global do DOCS.\n",
        docs_root / "references" / "history" / "abandoned-index.md": "# abandoned-index\n\nHistorico residual de planos abandonados.\n",
        docs_root / "references" / "_generated" / "context-registry-bootstrap.json": dump_json(
            {
                "generated_at_utc": None,
                "purpose": "bootstrap placeholder created by docs-init",
                "records": [],
                "summary": {"bucket_counts": {}, "display_type_counts": {}, "total_records": 0},
                "usage": ["filter by topic or name", "open best_entry_path", "expand only when needed"],
            }
        )
        + "\n",
        docs_root / "references" / "_generated" / "context-registry.json": dump_json(
            {"generated_at_utc": None, "purpose": "full registry placeholder created by docs-init", "records": []}
        )
        + "\n",
        docs_root / "references" / "_generated" / "context-registry-for-humans" / "README.md": "# context-registry-for-humans\n\nEspelho humano gerado por bucket.\n",
        docs_root / "references" / "_generated" / "agent-audit" / "README.md": "# agent-audit\n\nRuns globais de auditoria de agentes.\n",
    }
    for path, content in files.items():
        if write_file_if_missing(path, content):
            created.append(str(path))

    return created


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clone, scaffold, or validate DOCS-Engenharia-de-Contexto.")
    parser.add_argument("--repo-path", help="Repo root or DOCS root. Defaults to the current working directory.")
    parser.add_argument("--remote", default=DOCS_REMOTE_URL, help=f"Remote used when cloning. Defaults to {DOCS_REMOTE_URL}.")
    parser.add_argument("--no-clone", action="store_true", help="Scaffold the minimum DOCS tree instead of cloning.")
    return parser.parse_args()


def clone_docs(remote: str, docs_root: Path) -> bool:
    if shutil.which("git") is None:
        return False

    docs_root.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(["git", "clone", "--depth", "1", remote, str(docs_root)], capture_output=True, text=True, check=False)
    return result.returncode == 0


def main() -> int:
    args = parse_args()
    try:
        repo_root = resolve_repo_root(repo_path=args.repo_path)
        docs_root = repo_root / DOCS_DIR_NAME

        normalized_entries: list[str] = []
        if docs_root.exists():
            action = "validated"
        elif not args.no_clone and clone_docs(args.remote, docs_root):
            action = "cloned"
            normalized_entries = normalize_docs(docs_root)
        else:
            action = "scaffolded"
            docs_root.mkdir(parents=True, exist_ok=True)
            normalized_entries = normalize_docs(docs_root)

        errors, warnings = validate_docs_root(docs_root)
        payload = {
            "action": action,
            "docs_root": str(docs_root),
            "errors": errors,
            "normalized_entries": normalized_entries,
            "repo_root": str(repo_root),
            "valid": not errors,
            "warnings": warnings,
        }
        print(dump_json(payload))
        return 0 if not errors else 1
    except ScriptError as exc:
        print(dump_json({"error": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
