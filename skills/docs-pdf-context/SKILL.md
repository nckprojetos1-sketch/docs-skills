---
name: docs-pdf-context
description: Extract and synthesize a requirements PDF into a DOCS context package. Use when the user invokes `$docs-pdf-context`, provides a PDF of software requirements, or asks to prepare PDF context for later `$docs-plan-ap` or `$docs-plan-sddr` planning.
---

# docs-pdf-context

Use this skill to transform a software requirements PDF into a compact, reliable DOCS context package.

This is a context-preparation skill. Do not create APs, SDDRs, PRDs, SPECs, or execution plans. The output feeds `$docs-plan-ap` or `$docs-plan-sddr` later.

## Inputs

- A PDF path is required.
- An output directory is optional.

Default output:

- If the repository has `DOCS-Engenharia-de-Contexto/`, write to `DOCS-Engenharia-de-Contexto/references/global/<pdf-slug>/`.
- If DOCS is not installed, write to `<pdf-slug>/` beside the PDF.
- If the user provides `--out`, use exactly that directory.

## Required Workflow

1. Validate the PDF path and confirm it is a readable `.pdf` file.
2. Run the extractor:

   ```powershell
   python skills\docs-pdf-context\scripts\extract_pdf_context.py <pdf-path>
   ```

   Use `--out <directory>` when the user requested a specific output directory.

3. Read `context.json`, `README.md`, and `tables.json` when present.
4. Load `references/readme-synthesis.md` before revising the README.
5. Rewrite or tighten `README.md` when the extractor draft is not a polished handoff. The README must be understandable by a later planning agent without opening the PDF.
6. Keep `tables.json` as audit support and preserve all `table_id` / `row_id` references cited by README.
7. Report created files and any extraction limitation.

## Output Contract

The package must include:

- `README.md`: the primary, autossuficient context handoff.
- `context.json`: intermediate extraction context for agent review.
- `tables.json`: only when real tables are detected.

`README.md` must contain:

- source document metadata;
- executive/system objective;
- audience/users;
- MVP scope and out of scope;
- functional requirements with ID, acceptance criterion, source page, and table/row reference when available;
- non-functional requirements grouped by UX, performance, security, deploy/versioning, and observability;
- endpoints, parameters, integrations, and important fields;
- explicit use cases or inferred flows, marking inference;
- deliverables and MVP acceptance checklist;
- risks, constraints, decisions, and open questions only when present in the PDF or when extraction has a real limitation;
- compact page traceability.

`tables.json` must contain only real tabular data. Narrative blocks detected by PyMuPDF as one-row tables are callouts in `context.json` and README, not table rows.

## Quality Checks

Before returning to the user, verify:

- all readable PDF pages are represented in traceability;
- all detected requirement IDs appear in README;
- every `table_id` in `tables.json` is cited in README;
- table rows used by README cite `table_id/row_id`;
- false table positives are reclassified as callouts;
- no placeholder, TODO, raw `_ _` artifacts, or artificial gaps remain;
- scanned or unreadable PDFs fail with a clear limitation instead of invented context.

## Boundaries

- Do not run OCR in v1.
- Do not call external LLM APIs from the script.
- Do not promote the extracted context into a plan automatically.
- Do not create AP, SDDR, PRD, SPEC, or dependencies files.
