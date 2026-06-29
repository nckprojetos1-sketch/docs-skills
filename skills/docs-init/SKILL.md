---
name: docs-init
description: Persistent DOCS environment entrypoint and router. Bootstrap, normalize, or validate `DOCS-Engenharia-de-Contexto` in a repository, then route user requests to the correct DOCS method skill. Use when the user says `/docs-init`, invokes `$docs-init`, asks to iniciar/preparar/validar um ambiente DOCS, works inside a repository with DOCS, or when another DOCS skill detects that the repository does not contain the DOCS root.
---

# docs-init

Treat `/docs-init` as a textual alias for this skill, not as a shell command.

This is the persistent entrypoint for the DOCS method. Do not treat this skill as disposable and do not ask to remove it after use.

## Bootstrap Workflow

1. Resolve the target repository root from the current working directory or the path the user gave.
2. Run `python scripts/docs_init.py [--repo-path <path>]`.
3. If `DOCS-Engenharia-de-Contexto` is missing, copy the canonical DOCS source bundled with this package when available, excluding `.git`, then normalize missing minimum entries.
4. If the DOCS root already exists, normalize only missing entries. Never overwrite existing DOCS files.
5. Report `repo_root`, `docs_root`, action, validation errors, warnings, and normalized entries.

## Environment Behavior

- If invoked only to initialize or validate, stop after the bootstrap report.
- If invoked with a work request and DOCS is valid, route the request to the correct DOCS skill.
- If another DOCS skill routed here because DOCS is missing, initialize DOCS and continue with the original intent when it is clear.
- If intent is clear, continue in the same turn by loading and following the selected sibling skill.
- If intent is ambiguous and the choice changes the path, inspect the minimum DOCS bootstrap and ask one concise question.
- If the selected sibling skill cannot be found or loaded, return an explicit handoff telling the user which skill to invoke.

## Required Bootstrap For Routing

When the request is not only initialization, read in this order:

1. `DOCS-Engenharia-de-Contexto/help/bootstrap-core.md`
2. `DOCS-Engenharia-de-Contexto/references/README.md`
3. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-bootstrap.json`
4. `best_entry_path` for the topic, when found
5. `context-registry.json` only when the bootstrap index is not enough
6. human bucket mirror only when the search is still broad
7. correlated code areas when needed to confirm whether an existing plan owns the work

Read `references/docs-method-core.md` only when the repo's own DOCS files are missing detail or you need a compact refresher.

## Routing Rules

Load the sibling skill's `SKILL.md` and follow it.

- Use `$docs-plan-sddr` when the user explicitly asks for SDDR, or asks for a new small/local/bounded change with no defensible owner plan.
- Use `$docs-plan-ap` when the user explicitly asks for AP, or wants a complex, structural, multi-module, multi-stage, or architecture-level plan.
- Use `$docs-executor` when the user asks to implement, fix, update, or execute work that is already planned/documented, especially a simple change tied to an existing plan.
- Use `$docs-analyze` when the owner plan is unclear, the user asks where context lives, or the request needs a recommendation between existing plan, SDDR, and AP.
- Use `$docs-reviewer` when the user asks to review DOCS structure, indexes, history, or method coherence.
- Use `$docs-clean-plan-context` when the user asks to consolidate or remove obsolete PRD/SPEC context after a completed SDDR or AP subplan.
- Use `$docs-pdf-context` when the user provides or references a requirements PDF and wants context prepared for later planning.

Do not automatically choose a skill when the request lacks enough signal. Ask only for the missing decision that changes routing.

## Sibling Skill Loading

Try these locations for the selected skill, in order:

1. a sibling directory next to this installed skill
2. `~/.codex/skills/<skill-name>/SKILL.md`
3. `~/.agents/skills/<skill-name>/SKILL.md`
4. repository source path `skills/<skill-name>/SKILL.md`

After loading the sibling skill, obey its workflow and mutation rules. The sibling skill becomes the operative contract for the rest of the turn.

## DOCS Contract

Minimum DOCS root entries:

- `README.md`
- `help/`
- `references/`
- `plans-to-be-executed/`
- `plans-executed/`
- `plans-abandoned/`

Minimum generated registry entries:

- `references/_generated/context-registry-bootstrap.json`
- `references/_generated/context-registry.json`
- `references/_generated/context-registry-for-humans/`

## Output

For bootstrap-only requests, return:

- detected `repo_root`
- detected `docs_root`
- action: `validated`, `normalized`, `copied-and-normalized`, `cloned`, or `scaffolded`
- whether the DOCS root is valid
- validation errors and warnings
- any created or normalized files

For routed work, start with a short note containing:

- bootstrap action
- selected DOCS skill
- why it was selected
- any remaining question, only if routing cannot be decided safely

## Resources

- `scripts/docs_init.py`
- `scripts/common.py`
- `references/docs-method-core.md`
