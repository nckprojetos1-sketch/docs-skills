from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DOCS_DIR_NAME = "DOCS-Engenharia-de-Contexto"


class ScriptError(RuntimeError):
    pass


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        raise ScriptError("Could not derive a slug.")
    return slug


def resolve_repo_root(repo_path: str | None) -> Path:
    candidate = Path(repo_path or Path.cwd()).expanduser().resolve()
    if candidate.name == DOCS_DIR_NAME:
        return candidate.parent
    if (candidate / DOCS_DIR_NAME).is_dir():
        return candidate
    if repo_path is not None:
        raise ScriptError(f"DOCS root not found at {candidate / DOCS_DIR_NAME}. Run docs-init first.")
    for parent in [candidate, *candidate.parents]:
        if (parent / DOCS_DIR_NAME).is_dir():
            return parent
        if parent.name == DOCS_DIR_NAME:
            return parent.parent
    raise ScriptError(f"DOCS root not found from {candidate}. Run docs-init first.")


def write_new(path: Path, content: str) -> None:
    if path.exists():
        raise ScriptError(f"Refusing to overwrite existing path: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a canonical DOCS SDDR.")
    parser.add_argument("--repo-path", help="Repo root or DOCS root. Defaults to cwd.")
    parser.add_argument("--name", required=True, help="SDDR name.")
    parser.add_argument("--objective", default="", help="Short objective.")
    parser.add_argument("--with-dependencies", action="store_true", help="Create dependencies.md.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo_root = resolve_repo_root(args.repo_path)
        docs_root = repo_root / DOCS_DIR_NAME
        plan_root = docs_root / "plans-to-be-executed" / f"{slugify(args.name)}__sddr"
        if plan_root.exists():
            raise ScriptError(f"SDDR already exists: {plan_root}")

        (plan_root / "reports").mkdir(parents=True)
        (plan_root / "references" / "agent-audit").mkdir(parents=True)
        write_new(
            plan_root / "status.md",
            f"status: draft\n\n## Objetivo\n{args.objective or 'Registrar o estado oficial do SDDR.'}\n\n## Checklist inicial\n- [ ] objetivo definido\n- [ ] escopo definido\n- [ ] handoff para executor pronto\n",
        )
        write_new(
            plan_root / "prd.md",
            "# PRD\n\n## Contexto\nDescrever o problema.\n\n## Objetivo\nExplicar o que a mudanca precisa entregar.\n\n## Escopo\n- o que entra\n- o que fica fora\n\n## Criterios de aceite\n- criterio 1\n- criterio 2\n",
        )
        write_new(
            plan_root / "spec.md",
            "# SPEC\n\n## Arquivos alvo\n- listar arquivos ou areas alvo\n\n## Contratos impactados\n- listar contratos relevantes\n\n## Fluxo tecnico\nDescrever a implementacao planejada.\n\n## Validacoes\n- comando 1\n- comando 2\n",
        )
        write_new(plan_root / "reports" / "README.md", "# reports\n\nProvas de execucao e handoffs deste SDDR.\n")
        write_new(plan_root / "references" / "agent-audit" / "README.md", "# agent-audit\n\nMemoria operacional curta das runs deste SDDR.\n")
        if args.with_dependencies:
            write_new(plan_root / "dependencies.md", "# dependencies\n\n## Dependencias explicitas\n- listar dependencias\n\n## Bloqueios conhecidos\n- nenhum, se nao houver\n")

        print(json.dumps({"sddr_root": str(plan_root), "dependencies": args.with_dependencies}, ensure_ascii=True, indent=2))
        return 0
    except ScriptError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
