---
name: docs-analyze
description: Analyze a user request against the DOCS method to find the plan that owns the relevant context before execution. Use when the user invokes `$docs-analyze`, asks which DOCS plan is responsible for a change, wants to know where PRD/SPEC/REPORTS must be updated, or needs a recommendation between creating an SDDR or AP because no owner plan is clear.
---

# docs-analyze

Use this skill only in a repository that contains `DOCS-Engenharia-de-Contexto/`. If it is missing, stop and route to `$docs-init`.

This is a diagnostic skill. Do not edit files, do not execute the requested change, and do not create plans.

## Zero-Text Entry

If invoked without extra instructions:

1. Confirm DOCS exists.
2. Read the minimum DOCS bootstrap.
3. Inspect the bootstrap registry and active plan roots.
4. Ask one concise question that closes the missing topic: the user request, affected area, or desired outcome.

The goal is to identify the best owner plan for the requested work before any execution starts.

## Required Bootstrap

Read, in this order:

1. `DOCS-Engenharia-de-Contexto/help/bootstrap-core.md`
2. `DOCS-Engenharia-de-Contexto/references/README.md`
3. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-bootstrap.json`
4. `best_entry_path` for the topic, when found
5. `context-registry.json` only when the bootstrap index is not enough
6. human bucket mirror only when the search is still broad
7. `help/conventions.md` only for structural or governance conflicts
8. relevant plan, subplan, SDDR, and correlated code areas

Read `references/docs-method-core.md` only when the repo's own DOCS files are missing detail or you need a compact refresher. Read `references/owner-selection.md` before selecting the owner plan.

## Matching Rules

- Treat live code as the highest truth for confirming the request topic.
- Use `references/_generated/context-registry-bootstrap.json` as the cheap index into likely plans and topics.
- Consider `plans-to-be-executed/` and `plans-executed/` as valid owner candidates for this skill.
- Treat `plans-abandoned/` as historical evidence only. Never select it as the mutable owner path.
- Prefer the narrowest owner that already contains the context:
  - SDDR root when the work belongs to one bounded plan
  - AP subplan root when the work belongs to a specific `NN-name__sp`
  - AP root only when the request is truly cross-subplan
- Never choose an owner only from naming similarity. Confirm with plan content, related code, or registry evidence.

## Analyze Workflow

1. Normalize the user request into topic, desired change, and likely affected code area.
2. Use the bootstrap registry to find likely records, `best_entry_path`, and related plan paths.
3. Inspect the strongest candidate plans in `plans-to-be-executed/` and `plans-executed/`.
4. Read the relevant `status.md`, `prd.md`, `spec.md`, `reports/`, or `xx-sddd/` needed to confirm ownership.
5. Inspect the correlated code or repository area cited by the request.
6. Select one primary owner path and list any related supporting plans.
7. If no owner is defensible, recommend opening a new plan:
   - `SDDR` for local, small, or bounded work
   - `AP` for structural, multi-front, or decomposed work

## Output Contract

Return a short diagnostic summary with:

- `request_summary`
- `primary_owner_path`
- `related_plan_paths`
- `evidence_consulted`
- `doc_update_targets`
- `recommendation`

`recommendation` must be exactly one of:

- `use-existing-plan`
- `create-sddr`
- `create-ap`

## Doc Update Targets

When an owner exists, specify exactly which DOCS artifacts a later executor must update.

For SDDR owners:

- `prd.md`
- `spec.md`
- `reports/`
- `status.md` only if the real state changes
- `dependencies.md` only if the new request introduces an explicit dependency

For AP subplan owners:

- the relevant `xx-sddd/prd.md`
- the relevant `xx-sddd/spec.md`
- the subplan root `reports/`
- the subplan root `status.md` only if the real state changes
- the relevant `xx-sddd/dependencies.md` only if the new request introduces an explicit dependency

For AP root owners:

- the affected subplan paths that must be updated
- AP-level documents only when the request changes cross-subplan architecture or sequencing

Do not update or recommend updates inside `plans-abandoned/`.

## Decision Standard

- Choose one primary owner path plus related plan paths when needed.
- Explain why the primary owner is the best match.
- If `plans-executed/` is the best owner, say so explicitly and treat it as updateable for this skill's workflow.
- If no plan is strong enough, prefer a clear recommendation over a weak match.
