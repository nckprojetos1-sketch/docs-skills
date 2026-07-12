# 05 — Anatomia de um AP (Architecting Plan)

Um AP é o pacote completo para trabalho estrutural. Ele decompõe um objetivo grande em **subplanos**
executáveis e consolida tudo em relatórios finais.

---

## Estrutura completa

```text
<nome>__ap/
├── status.md                          # estado oficial do AP
├── architecting-plan/                 # o planejamento arquitetural
│   ├── 01-vision.md                   # visão e objetivo macro
│   ├── 02-scope-and-modules.md        # escopo e módulos impactados
│   ├── 03-dependencies.md             # dependências entre frentes
│   └── 04-execution-and-merge.md      # ordem de execução e estratégia de merge
├── final-reports/                     # consolidação final (gate → plans/04-completed/)
│   ├── report-final.md                # MESTRE (obrigatório) — indexa os anexos
│   ├── report-final-execucao.md
│   ├── report-final-arquitetura-e-contratos.md
│   ├── report-final-riscos-e-pendencias.md
│   └── final-reports-checklist.md     # checklist estrito de migração
├── references/
│   └── agent-audit/                   # gaveta de runs deste AP
└── NN-nome__sp/                       # um ou mais subplanos (01-, 02-, ...)
    ├── status.md                      # ← autoridade de estado do subplano
    ├── 01-sddd/                       # etapa local de planejamento+execução
    │   ├── prd.md
    │   ├── spec.md
    │   └── dependencies.md
    ├── references/                    # prompt de execução + material de apoio
    │   └── execution-prompt.md
    └── reports/                       # prova de execução e handoffs do subplano
```

> **Nota sobre `references/` no subplano.** O método canônico original define o subplano apenas com
> `status.md` + `reports/` + `01-sddd/`. **Neste repositório** convencionou-se guardar o **prompt de
> execução** (`execution-prompt.md`) e o material de apoio dentro de uma pasta `references/` de cada
> subplano. Portanto, todo subplano aqui tem, no mínimo, `01-sddd/` + `references/` + `reports/` +
> `status.md`. Este guia documenta a convenção **como praticada**.

---

## Regras dos subplanos

- Todo subplano **nasce com `01-sddd/`**.
- `02-sddd/`, `03-sddd/`... só surgem quando a etapa anterior **não cobre** o trabalho.
- Os `reports/` ficam na **raiz do subplano**, nunca dentro de um `xx-sddd/`.
- O **`status.md` da raiz do `__sp`** é o estado oficial daquele subplano.
- Não existe mais `backup-plans/` em AP.

---

## O que cada etapa (`xx-sddd`) contém

| Arquivo | Papel |
| --- | --- |
| `prd.md` | O **que** entregar: contexto, objetivo, escopo, critérios de aceite. |
| `spec.md` | **Como** entregar: arquivos alvo, contratos, fluxo técnico, validações. |
| `dependencies.md` | Dependências explícitas e bloqueios conhecidos (obrigatório). |

---

## Exemplo real: `nfx-rebuild__ap`

Este repositório tem um AP ativo em
`plans/03-running/nfx-rebuild__ap`, com **16 subplanos numerados**:

```text
nfx-rebuild__ap/
├── architecting-plan/     (01-vision, 02-scope-and-modules, 03-dependencies,
│                           04-subplans, 05-execution-and-merge)
├── final-reports/
├── references/            (agent-audit/, execution-references/, prompts/, ...)
├── 01-base-tecnica-runtime-plataforma__sp
├── 02-conexao-banco-migracoes__sp
├── 03-autenticacao-tenants-usuarios-empresas-certificados__sp
├── ...
├── 14-dre__sp
├── 15-frontend-ap__sp
└── 16-build-docker-compose__sp
```

Cada um desses 16 subplanos segue o padrão **`01-sddd/` + `references/` + `reports/` + `status.md`**,
com o `execution-prompt.md` dentro de `references/`. Um subplano típico:

```text
01-base-tecnica-runtime-plataforma__sp/
├── status.md
├── 01-sddd/
│   ├── prd.md
│   ├── spec.md
│   └── dependencies.md
├── references/
│   └── execution-prompt.md      # prompt de contexto limpo do executor
└── reports/
    └── 2026-06-18__execution-report.md
```

---

## O `status.md` de um subplano (formato real)

Além da primeira linha `status:`, um `status.md` de subplano costuma trazer, em Markdown:

- um bloco de metadados (`Status`, `Execution status`, `Documentation status`, `Updated`, `Source`);
- seções: **Objetivo**, **Readiness**, **Documentos obrigatórios**, **Resultado de execução**
  (com link para o report em `reports/`), **Completion Gate** (checklist de aceite), **Blocks**,
  **Anti-Regression**.

Ele é, ao mesmo tempo, o rastreador de estado e o *gate* de aceite do subplano.

---

## O pacote `final-reports/` e o gate para `plans/04-completed/`

Um AP só vai para `plans/04-completed/` quando o pacote de `final-reports/` está completo:

- `report-final.md` **(mestre, obrigatório)** — 11 seções, incluindo um **mapa de rastreabilidade**
  ligando `architecting-plan/*`, subplanos executados, reports por subplano, `references/*` e
  evidências;
- os três anexos (execução, arquitetura-e-contratos, riscos-e-pendências);
- o `final-reports-checklist.md`, com o *gate* estrito marcado item a item.

Ver os esqueletos prontos em [`../templates/__ap/final-reports/`](../templates/__ap/final-reports/).
