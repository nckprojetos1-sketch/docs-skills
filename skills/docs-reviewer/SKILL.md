---
name: docs-reviewer
description: Review DOCS method coherence, registry/index quality, references curation, history, abandoned plans, and PTBE/PE/PA movements. Use when the user invokes `$docs-reviewer`, asks to revisar o metodo DOCS, audit references, triage context, validate indexes, or inspect documentation consistency. Not for product code review.
---

# docs-reviewer

Use this skill only in a repository that contains `DOCS-Engenharia-de-Contexto/`. If it is missing, stop and route to `$docs-init`.

This is a DOCS method reviewer. It is not a product code review skill.

## Zero-Text Entry

If invoked without extra text:

1. Confirm DOCS exists.
2. Read the reviewer bootstrap.
3. Inspect registry and active plan structure at a high level.
4. Ask what the user wants reviewed: index, references/global, history, plan movement, active plan consistency, or full method coherence.

Ask targeted questions only when they change the review decision.

## Required Bootstrap

Read, in this order:

1. `DOCS-Engenharia-de-Contexto/help/bootstrap-core.md`
2. `DOCS-Engenharia-de-Contexto/references/README.md`
3. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-bootstrap.json`
4. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry.json`
5. human bucket mirror when broad triage helps
6. `references/history/abandoned-index.md`
7. `references/global/` when repo-wide documents are involved
8. `help/conventions.md` when the review touches structure, DoD, or governance
9. `help/inits/init-agents/init-reviewer-agent.md`, then follow it as the repo-specific contract

## Review Decisions

Every reviewed item must end with one clear decision:

- `promover para global`
- `manter no plano`
- `mover para plans-abandoned`
- `corrigir o indice`

Include:

- justification
- risk
- evidence consulted
- recommended next step

## Audit

Use global audit by default:

- `DOCS-Engenharia-de-Contexto/references/_generated/agent-audit/YYYY-MM-DD__reviewer__slug/run.md`

Use plan audit only when the review is restricted to one plan:

- `<plano>/references/agent-audit/YYYY-MM-DD__reviewer__slug/run.md`

Do not put handoff in `agent-audit`; handoff belongs in `reports/` or the final response.

## Output

Return findings first, grouped by severity or method risk. Then list open questions and recommended corrections.

Read `references/docs-method-core.md` for the compact method summary.
