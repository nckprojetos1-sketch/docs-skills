---
name: docs-executor
description: Execute technical or documentation changes under the DOCS method. Use when the user invokes `$docs-executor`, asks an agent to executar uma mudanca, implementar, corrigir, atualizar planos ativos, maintain DOCS operational documentation, or continue work tied to a DOCS plan/subplan/SDDD.
---

# docs-executor

Use this skill only in a repository that contains `DOCS-Engenharia-de-Contexto/`. If it is missing, stop and route to `$docs-init`.

## Zero-Text Entry

If invoked without extra instructions:

1. Confirm DOCS exists.
2. Read the minimum DOCS bootstrap.
3. Inspect `plans-to-be-executed/` and the bootstrap registry.
4. Identify likely active work.
5. Ask a concise question that closes the missing execution scope: target plan, desired change, expected validation, or whether to create a new plan first.

Be objective, clear, and direct. The skill should guide the conversation toward a complete execution contract before changing files.

## Required Bootstrap

Read, in this order:

1. `DOCS-Engenharia-de-Contexto/help/bootstrap-core.md`
2. `DOCS-Engenharia-de-Contexto/references/README.md`
3. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-bootstrap.json`
4. `best_entry_path` for the topic, when found
5. `context-registry.json` only when the bootstrap index is not enough
6. human bucket mirror only when the search is still broad
7. `help/conventions.md` only for structural, governance, DoD, or method conflicts
8. `help/inits/init-agents/init-executor-agent.md`, then follow it as the repo-specific contract

## Execution Rules

- Treat live code as highest truth.
- Treat the relevant plan, subplan, or SDDD as the execution contract.
- Treat `references/` as an index and global support, not as a substitute for plan or code.
- Do not read the full registry by default.
- Do not promote content to `references/` unless it is repo-wide or changes navigation.
- Do not write handoff into `agent-audit`; put handoff in `reports/` or the final answer.

## Before Mutating

Close these points:

- target plan/subplan/SDDD, or confirm the work is transversal;
- intended user-visible change;
- files or areas likely touched;
- expected validations;
- whether `status.md`, `reports/`, `references/`, or `agent-audit` must be updated.

## After Execution

Evaluate and update only when applicable:

- `status.md`
- `reports/`
- `references/_generated/context-registry-bootstrap.json`
- `references/_generated/context-registry.json`
- `references/_generated/context-registry-for-humans/`
- `references/history/abandoned-index.md`
- `references/global/`
- `references/agent-audit/YYYY-MM-DD__executor__slug/run.md` or global audit when the run is transversal

## Output

Start execution with a short bootstrap summary:

- topic found
- `best_entry_path`
- target plan/subplan/SDDD
- code area to inspect
- whether the full registry was needed

Read `references/docs-method-core.md` only when the repo's own DOCS files are missing detail or you need a compact refresher.
