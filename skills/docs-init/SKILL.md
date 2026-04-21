---
name: docs-init
description: Bootstrap or validate `DOCS-Engenharia-de-Contexto` in a repository using the current DOCS method. Use when the user says `/docs-init`, invokes `$docs-init`, asks to install/preparar/validar DOCS in a repo, or when another DOCS skill detects that the repository does not contain the DOCS root.
---

# docs-init

Treat `/docs-init` as a textual alias for this skill, not as a shell command.

## Workflow

1. Resolve the target repository root from the current working directory or the path the user gave.
2. Run `python scripts/docs_init.py [--repo-path <path>]`.
3. If `DOCS-Engenharia-de-Contexto` is missing, clone the official DOCS source when possible and normalize the current canonical entries.
4. If the DOCS root already exists, validate only. Do not pull, overwrite, or rewrite existing DOCS content unless the user explicitly asks.
5. Report the action, `repo_root`, `docs_root`, validation errors, warnings, and normalized entries.

## Conversation Behavior

- If invoked without extra text, inspect the current directory and validate or bootstrap that repository.
- If the current directory is ambiguous, ask for the target repo path in one concise question.
- If a repository already has DOCS, explain that this skill validates structure and does not update the method automatically.
- If another DOCS skill routed here because DOCS is missing, return a short next step telling the user to rerun the original skill after initialization.

## DOCS Contract

Read `references/docs-method-core.md` when you need the current method summary.

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

Return:

- detected `repo_root`
- detected `docs_root`
- action: `validated`, `cloned`, or `scaffolded`
- whether the DOCS root is valid
- validation errors and warnings
- any created or normalized files

## Resources

- `scripts/docs_init.py`
- `scripts/common.py`
- `references/docs-method-core.md`
