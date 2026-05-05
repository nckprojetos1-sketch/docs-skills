# README Synthesis Contract

Use this reference after running `scripts/extract_pdf_context.py`.

The extractor gives a strong draft, but the agent remains responsible for the final README quality. Rewrite only from `context.json`, `tables.json`, and the generated README. Do not invent product scope.

## Primary Goal

The README must be a handoff document that lets a later `$docs-plan-ap` or `$docs-plan-sddr` agent understand the system requirements without opening the PDF.

## Writing Rules

- Write in clear Portuguese.
- Prefer product and engineering meaning over PDF order.
- Preserve source references as `p.N`, `table_id`, and `row_id`.
- Mark inferred flows or decisions with `Inferido:`.
- Keep tables in JSON; summarize table meaning in README.
- Remove extraction noise such as repeated headers, broken line fragments, isolated `_`, and section labels without content.

## Required Sections

1. Metadados
2. Visao Executiva
3. Escopo do MVP
4. API, Endpoints, Parametros e Uso
5. Requisitos Funcionais
6. Requisitos Nao Funcionais
7. Arquitetura Minima e Componentes
8. Dados e Campos Para Implementacao
9. Fluxos De Uso
10. Criterios De Aceite Do MVP
11. Entregaveis Esperados
12. Callouts E Decisoes Narrativas
13. Indice De Tabelas Estruturadas
14. Rastreabilidade Por Pagina

## Acceptance Standard

- A later agent can plan implementation from README alone.
- `tables.json` remains useful for audit and exact table recovery.
- Every functional requirement ID from the PDF appears exactly once in the functional requirements section.
- Every table in `tables.json` is referenced in the README table index and at least one content section.
