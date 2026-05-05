---
name: docs-pdf-context
description: Extract a requirements PDF into a compact DOCS context package. Use when the user invokes `$docs-pdf-context`, provides a PDF of requirements, or asks to prepare PDF context for later `$docs-plan-ap` or `$docs-plan-sddr` planning.
---

# docs-pdf-context

Use this skill to transform a requirements PDF into a compact context package for the DOCS method.

This is a context-preparation skill. Do not create APs, SDDRs, PRDs, SPECs, or execution plans. The output is intended to feed `$docs-plan-ap` or `$docs-plan-sddr` later.

## Inputs

- A PDF path is required.
- An output directory is optional.

Default output:

- If the repository has `DOCS-Engenharia-de-Contexto/`, write to `DOCS-Engenharia-de-Contexto/references/global/<pdf-slug>/`.
- If DOCS is not installed, write to `<pdf-stem>-context/` beside the PDF.
- If the user provides `--out`, use exactly that directory.

## Required Workflow

1. Validate the PDF path and confirm it is a readable `.pdf` file.
2. Run the extractor:

   ```powershell
   python skills\docs-pdf-context\scripts\extract_pdf_context.py <pdf-path>
   ```

   Use `--out <directory>` when the user requested a specific output directory.

3. Read the generated `README.md` and, when present, `tables.json`.
4. Check that the package is compact, concrete, and traceable to pages or sections.
5. Report the created files and any extraction limitation from the script output.

## Output Contract

The package must always include `README.md` with:

- source document metadata;
- system objective;
- audience/users;
- MVP scope;
- out of scope;
- functional requirements;
- non-functional requirements grouped by UX, performance, security, deploy, versioning, and observability;
- endpoints, parameters, and integrations mentioned in the PDF;
- important implementation data and fields;
- explicit use cases or inferred flows, marking inference when the PDF does not name use cases;
- acceptance criteria;
- risks, constraints, and open questions only when present in the PDF or when a real extraction gap exists;
- page/section traceability.

Create `tables.json` only when real tables are detected. It must contain normalized table rows in a stable structure:

```json
{
  "tables": [
    {
      "page": 2,
      "table_index": 1,
      "title_or_context": "Recurso / Endpoint / Uso minimo",
      "columns": ["Recurso", "Endpoint / parametro", "Uso minimo no sistema"],
      "rows": [
        {
          "Recurso": "Listar produtos",
          "Endpoint / parametro": "GET /v2/products",
          "Uso minimo no sistema": "Fonte principal da tela de catalogo..."
        }
      ]
    }
  ]
}
```

## Quality Checks

Before returning to the user, verify:

- all readable PDF pages are represented in traceability;
- all detected requirement IDs appear in `README.md`;
- detected tables are represented in `tables.json`;
- relevant PDF sections are reflected in `README.md`;
- no placeholder, TODO, or artificial gap was introduced;
- scanned or unreadable PDFs fail with a clear limitation instead of invented context.

## Boundaries

- Do not run OCR in v1.
- Do not promote the extracted context into a plan automatically.
- Do not create AP, SDDR, PRD, SPEC, or dependencies files.
- Keep `tables.json` as structured preservation only; `README.md` remains the operational context.
