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


def normalize_subplan(raw: str, index: int) -> str:
    raw = raw.strip()
    match = re.match(r"^(?P<num>\d{2})[-_ ]+(?P<rest>.+)$", raw)
    if match:
        return f"{match.group('num')}-{slugify(match.group('rest'))}__sp"
    return f"{index:02d}-{slugify(raw)}__sp"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a canonical DOCS AP.")
    parser.add_argument("--repo-path", help="Repo root or DOCS root. Defaults to cwd.")
    parser.add_argument("--name", required=True, help="AP name.")
    parser.add_argument("--objective", default="", help="Short AP objective.")
    parser.add_argument("--subplan", action="append", default=[], help="Subplan name. Can be passed multiple times.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo_root = resolve_repo_root(args.repo_path)
        docs_root = repo_root / DOCS_DIR_NAME
        plans_root = docs_root / "plans-to-be-executed"
        ap_name = f"{slugify(args.name)}__ap"
        ap_root = plans_root / ap_name
        if ap_root.exists():
            raise ScriptError(f"AP already exists: {ap_root}")

        subplans = args.subplan or ["01-execution"]
        subplan_names = [normalize_subplan(item, idx) for idx, item in enumerate(subplans, start=1)]

        (ap_root / "architecting-plan").mkdir(parents=True)
        (ap_root / "final-reports").mkdir(parents=True)
        (ap_root / "references" / "agent-audit").mkdir(parents=True)

        write_new(
            ap_root / "status.md",
            f"status: draft\n\n## Objetivo\n{args.objective or 'Definir e coordenar este AP.'}\n\n## Checklist inicial\n- [ ] objetivo do AP definido\n- [ ] subplanos iniciais criados\n- [ ] gaveta `references/agent-audit/` pronta\n- [ ] handoff para executor pronto\n",
        )
        for name, title in [
            ("architecting-plan-01-vision.md", "Visao"),
            ("architecting-plan-02-scope-and-modules.md", "Escopo e modulos"),
            ("architecting-plan-03-dependencies.md", "Dependencias"),
            ("architecting-plan-04-execution-and-merge.md", "Execucao e merge"),
        ]:
            write_new(ap_root / "architecting-plan" / name, f"# {title}\n\n")

        write_new(ap_root / "final-reports" / "README.md", "# final-reports\n\nConsolidacao final do AP.\n")
        write_new(ap_root / "references" / "agent-audit" / "README.md", "# agent-audit\n\nMemoria operacional curta das runs deste AP.\n")

        for subplan in subplan_names:
            sp_root = ap_root / subplan
            (sp_root / "reports").mkdir(parents=True)
            (sp_root / "01-sddd").mkdir(parents=True)
            write_new(
                sp_root / "status.md",
                "status: draft\n\n## Objetivo\nRegistrar o estado oficial do subplano.\n\n## Regra\n- este arquivo e a autoridade de estado do `__sp`\n- os `xx-sddd` detalham a etapa local\n- `reports/` documenta o que foi executado e os handoffs\n",
            )
            write_new(sp_root / "reports" / "README.md", "# reports\n\nProvas de execucao e handoffs deste subplano.\n")
            write_new(
                sp_root / "01-sddd" / "prd.md",
                "# PRD - 01-sddd\n\n## Contexto\nDescrever o problema local desta etapa do subplano.\n\n## Objetivo\nExplicar o que esta etapa precisa entregar.\n\n## Escopo\n- o que entra\n- o que fica fora\n\n## Criterios de aceite\n- criterio 1\n- criterio 2\n",
            )
            write_new(
                sp_root / "01-sddd" / "spec.md",
                "# SPEC - 01-sddd\n\n## Arquivos alvo\n- listar arquivos ou areas alvo\n\n## Contratos e interfaces impactados\n- listar contratos relevantes\n\n## Fluxo tecnico\nDescrever a execucao tecnica desta etapa.\n\n## Validacoes\n- comando 1\n- comando 2\n",
            )
            write_new(
                sp_root / "01-sddd" / "dependencies.md",
                "# dependencies - 01-sddd\n\n## Dependencias explicitas\n- listar dependencias desta etapa\n\n## Bloqueios conhecidos\n- nenhum, se nao houver\n",
            )

        print(json.dumps({"ap_root": str(ap_root), "subplans": subplan_names}, ensure_ascii=True, indent=2))
        return 0
    except ScriptError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
