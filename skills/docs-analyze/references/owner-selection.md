# Owner Selection

Use this reference to choose the DOCS plan that owns the context for a requested change.

## Goal

Pick the best existing owner before execution starts, so later work updates the right PRD, SPEC, and REPORTS instead of scattering truth.

## Candidate Sources

Search in this order:

1. `references/_generated/context-registry-bootstrap.json`
2. `best_entry_path`
3. `plans-to-be-executed/`
4. `plans-executed/`
5. `plans-abandoned/` as historical evidence only
6. correlated code and repository structure

Use the full registry and human bucket only when the bootstrap index is not enough.

## Candidate Priority

Prefer the strongest match using this order:

1. plan content that already describes the requested area
2. direct overlap with the affected code or module
3. evidence in `reports/` or prior execution history
4. recency and continuity of the plan
5. narrower ownership over broader ownership

## Narrowest Responsible Owner

Choose the smallest path that already contains the truth you need to extend:

- SDDR root for bounded local work
- AP subplan root for work clearly owned by one `NN-name__sp`
- AP root only when the request changes coordination across multiple subplans

Do not choose a path only because the folder name looks similar to the request.

## Special Policy For Analyze

For this skill only:

- `plans-to-be-executed/` can be selected as the owner
- `plans-executed/` can also be selected as the owner and treated as updateable
- `plans-abandoned/` can inform the diagnosis but must never be the mutable owner

If a completed plan is the best owner, state that it lives in `plans-executed/` and that later execution must update that plan's documentation instead of opening a weaker duplicate by default.

## Output Shape

Always return:

- one `primary_owner_path`
- zero or more `related_plan_paths`
- `evidence_consulted`
- `doc_update_targets`

If the evidence is weak, do not force a match. Recommend a new plan instead.

## Recommending A New Plan

Recommend `create-sddr` when the requested change is local, small, and bounded.

Recommend `create-ap` when the requested change is structural, multi-front, cross-module, or likely to require decomposition into subplans.

If `plans-abandoned/` contains useful prior context, mention it as historical evidence in the recommendation, but do not treat it as the owner.
