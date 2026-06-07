---
name: docs-clean-plan-context
description: Consolidate and remove obsolete planning context after DOCS implementation. Use when the user invokes `$docs-clean-plan-context`, asks to limpar PRD/SPEC depois da implementacao, remove useless SDDR/AP subplan planning files, or move useful semantic context from prd.md/spec.md into reports for a completed SDDR or completed AP subplan.
---

# docs-clean-plan-context

Use this skill only in a repository that contains `DOCS-Engenharia-de-Contexto/`. If it is missing, stop and route to `$docs-init`.

This is a post-implementation cleanup skill. It does not implement product changes.

## Purpose

After a DOCS plan is completed, `prd.md` and `spec.md` stop being the best
context entrypoint. The reports become the durable source for what happened.

This skill consolidates the useful semantic context from `prd.md` and `spec.md`
into a new report, then removes those planning files so future agents read the
completed reports instead of stale execution contracts.

## Required Bootstrap

Read, in this order:

1. `DOCS-Engenharia-de-Contexto/help/bootstrap-core.md`
2. `DOCS-Engenharia-de-Contexto/references/README.md`
3. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-bootstrap.json`
4. the target SDDR or AP subplan `status.md`
5. the target `reports/`
6. the target `xx-sddd/prd.md` and `xx-sddd/spec.md` pairs
7. `help/conventions.md` only for structural, DoD, or governance conflicts

Open the full registry only if the bootstrap index does not identify the target
or if removing the files changes navigation.

## Valid Targets

Operate only on one explicit target at a time:

- completed SDDR root with `status.md`, `reports/`, and one or more
  `xx-sddd/prd.md` plus `xx-sddd/spec.md` pairs;
- completed AP subplan `NN-*__sp/` with `status.md`, `reports/`, and one or more
  `xx-sddd/prd.md` plus `xx-sddd/spec.md` pairs.

For SDDRs and AP subplans, write the consolidation report to the target root `reports/`.
Do not write reports inside `xx-sddd/`.

## Hard Gates

Stop without deleting anything if:

- `status.md` is missing;
- status is not `completed`;
- `reports/` is missing or empty;
- no execution report explains what was implemented;
- `prd.md` or `spec.md` still appear to be needed for unfinished work;
- dependencies are unresolved;
- the useful semantic context cannot be separated from obsolete implementation
  instructions.

When blocked, explain what evidence is missing and which file must be completed
first.

## Consolidation Report

Create a new report before deleting files:

- SDDR: `<sddr>/reports/report-context-consolidation.md`
- AP subplan: `<subplan>/reports/report-context-consolidation.md`

If that file already exists, update it instead of creating a duplicate.

The report must include:

- original problem;
- objective;
- semantic solution or design direction;
- scope that remains useful for understanding the completed work;
- acceptance criteria that still explain why the result is valid;
- contracts, modules, or areas impacted in result-oriented language;
- references to the execution reports used as evidence;
- list of removed planning files.

Do not copy PRD/SPEC wholesale. Summarize only durable context. Drop obsolete
checklists, speculative implementation steps, temporary validation commands,
and instructions that were useful only before execution.

## Deletion Rules

Delete only after the consolidation report exists and has enough context to
replace PRD/SPEC as a reader entrypoint.

Allowed deletions:

- SDDR: each completed `xx-sddd/prd.md` and `xx-sddd/spec.md`
- AP subplan: each completed `xx-sddd/prd.md` and `xx-sddd/spec.md`

Never delete:

- `dependencies.md`;
- `status.md`;
- existing `reports/`;
- `references/agent-audit/`;
- AP `architecting-plan/`;
- AP `final-reports/`.

## Audit

Record the cleanup run in the target plan audit drawer:

- `<target>/references/agent-audit/YYYY-MM-DD__clean-plan-context__slug/run.md`

For AP subplans that do not have their own `references/agent-audit/`, use the AP
root audit drawer and name the target subplan in `run.md`.

The audit must record:

- target path;
- status evidence;
- reports consulted;
- consolidation report path;
- files removed;
- whether registry or references updates were needed.

Do not put handoff in `agent-audit`; the durable handoff is the consolidation
report and existing execution reports.

## References Updates

Update references only when navigation changes because PRD/SPEC had been indexed
as the best entrypoint.

When needed, update:

- `references/_generated/context-registry-bootstrap.json`
- `references/_generated/context-registry.json`
- `references/_generated/context-registry-for-humans/`

The new best entrypoint should be the consolidation report or the most complete
execution report, not the deleted PRD/SPEC.

## Output

Return:

- target cleaned;
- consolidation report path;
- planning files deleted;
- reports used as evidence;
- audit path;
- whether references/indexes were updated;
- any residual risks or skipped files.
