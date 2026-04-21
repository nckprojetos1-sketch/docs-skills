# DOCS Method Core

DOCS is a context engineering method for AI-oriented work. Documentation is operational infrastructure, not a byproduct.

## Truth Hierarchy

1. Live repository code.
2. Relevant plan, subplan, or SDDD.
3. `references/` as index and global support.
4. Remaining history.

`references/` points to context. It does not replace plans or code.

## Discovery Flow

Use cheap, directed bootstrap:

1. `DOCS-Engenharia-de-Contexto/references/README.md`
2. `references/_generated/context-registry-bootstrap.json`
3. `best_entry_path` for the topic
4. `context-registry.json` only when signals are missing
5. `context-registry-for-humans/<bucket>.md` only when broad search remains necessary
6. relevant plan, subplan, SDDD, and correlated code

Never start by reading the full registry by default.

## Official Roots

- `help/`: method, rules, inits, templates
- `references/`: short index and few global truths
- `plans-to-be-executed/`: active mutable execution
- `plans-executed/`: completed history
- `plans-abandoned/`: abandoned immutable history

## AP

Use AP for architecture-level, structural, or multi-front work.

Canonical AP root:

- `architecting-plan/`
- `status.md`
- `final-reports/`
- `references/agent-audit/`
- subplans `NN-name__sp`

Each AP subplan has `status.md`, `reports/`, and `01-sddd/`. Each `xx-sddd/` has `prd.md`, `spec.md`, and `dependencies.md`.

## SDDR

Use SDDR for local, small, or bounded work.

Canonical SDDR root:

- `prd.md`
- `spec.md`
- `status.md`
- `reports/`
- `references/agent-audit/`

`dependencies.md` exists in SDDR only when there is an explicit dependency.

## Status, Reports, Audit

Official statuses: `draft`, `ready`, `running`, `blocked`, `completed`.

- Every plan and subplan must have `status.md`.
- `reports/` stores execution proof and handoff.
- `agent-audit/` stores short operational memory for a run.
- Handoff never lives in `agent-audit`.

## DoD

A plan is completed only when contracts are fulfilled, dependencies are resolved, reports are complete, and `status.md` says `completed`.
