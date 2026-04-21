---
name: docs-plan-sddr
description: Open and document an SDDR plan under the DOCS method. Use when the user invokes `$docs-plan-sddr`, asks to abrir/criar/planejar um SDDR, needs planning for a small/local bounded change, or wants a non-executing planning conversation before implementation.
---

# docs-plan-sddr

Use this skill only in a repository that contains `DOCS-Engenharia-de-Contexto/`. If it is missing, stop and route to `$docs-init`.

This is a planner skill. Do not execute code.

## Zero-Text Entry

If invoked without extra text:

1. Confirm DOCS exists.
2. Read the minimum bootstrap and inspect active plans.
3. Explain that this skill opens an SDDR and will not execute.
4. Ask a focused first question that elicits the local problem, desired result, and acceptance criteria.

Guide the conversation to a compact but execution-ready PRD/SPEC.

## Required Bootstrap

Read, in this order:

1. `DOCS-Engenharia-de-Contexto/help/bootstrap-core.md`
2. `DOCS-Engenharia-de-Contexto/references/README.md`
3. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-bootstrap.json`
4. `context-registry.json` only if the bootstrap index is not enough
5. human bucket mirror only if the search is still broad
6. `help/conventions.md` only for structural or governance conflicts
7. `help/inits/init-agents/init-plan-sddr-agent.md`, then follow it as the repo-specific contract

## Planning Conversation

Close these before creating files:

- objective
- problem to solve
- scope boundaries
- risks and constraints
- acceptance criteria
- expected validation commands
- explicit dependencies, if any

Do not create `xx-sddd/` for SDDR. That structure belongs to AP subplans.

## Creating The SDDR

Use `python scripts/create_sddr.py --repo-path <repo> --name "<name>"` after the planning conversation has enough detail.

The SDDR must be created in `plans-to-be-executed/` with:

- `prd.md`
- `spec.md`
- `status.md`
- `reports/`
- `references/agent-audit/`

Create `dependencies.md` only when there is an explicit dependency.

## Final Output

Return:

- created SDDR path
- planning summary
- handoff for executor
- whether references/indexes need updates

Read `references/docs-method-core.md` for the compact method summary.
