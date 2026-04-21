---
name: docs-plan-ap
description: Open and document an Architecting Plan (AP) under the DOCS method. Use when the user invokes `$docs-plan-ap`, asks to abrir/criar/planejar um AP, needs architecture-level planning, multi-module coordination, decomposition into subplans, or a non-executing planning conversation before implementation.
---

# docs-plan-ap

Use this skill only in a repository that contains `DOCS-Engenharia-de-Contexto/`. If it is missing, stop and route to `$docs-init`.

This is a planner skill. Do not execute code.

## Zero-Text Entry

If invoked without extra text:

1. Confirm DOCS exists.
2. Read the minimum bootstrap and inspect active plans.
3. Explain that this skill opens an AP and will not execute.
4. Ask a focused first question that elicits the architecture problem, desired outcome, and known impacted areas.

Guide the conversation with clarity and personality, but keep every question useful. The goal is to produce the best possible planning documentation.

## Required Bootstrap

Read, in this order:

1. `DOCS-Engenharia-de-Contexto/help/bootstrap-core.md`
2. `DOCS-Engenharia-de-Contexto/references/README.md`
3. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-bootstrap.json`
4. `context-registry.json` only if the bootstrap index is not enough
5. human bucket mirror only if the search is still broad
6. `references/history/abandoned-index.md` only for abandonment or retomada topics
7. `help/conventions.md` only for structural or governance conflicts
8. `help/inits/init-agents/init-plan-ap-agent.md`, then follow it as the repo-specific contract

## Planning Conversation

Close these before creating files:

- objective and motivation
- problem statement
- scope boundaries and out-of-scope items
- impacted modules or areas
- acceptance criteria
- initial subplans and sequencing
- known dependencies, risks, and open questions

Do not go deeper into implementation than necessary for handoff. The AP should be execution-ready, not already executed.

## Creating The AP

Use `python scripts/create_ap.py --repo-path <repo> --name "<name>" --subplan "<subplan>" ...` after the planning conversation has enough detail.

The AP must be created in `plans-to-be-executed/` with:

- `status.md`
- `architecting-plan/`
- `final-reports/`
- `references/agent-audit/`
- subplans `NN-*__sp`

Each subplan must include:

- `status.md`
- `reports/`
- `01-sddd/prd.md`
- `01-sddd/spec.md`
- `01-sddd/dependencies.md`

## Final Output

Return:

- created AP path
- subplans created
- planning summary
- handoff for executor
- whether references/indexes need updates

Read `references/docs-method-core.md` for the compact method summary.
