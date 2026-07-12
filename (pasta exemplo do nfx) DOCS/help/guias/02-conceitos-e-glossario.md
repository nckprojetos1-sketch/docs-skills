# 02 — Conceitos e glossário

Este guia define, de forma curta, cada termo do método. Use-o como referência rápida.

---

## Os dois caminhos de trabalho

| Termo | Sufixo | O que é |
| --- | --- | --- |
| **AP — Architecting Plan** | `__ap` | Plano completo para trabalho **estrutural, grande ou multi-frente**, que se decompõe em subplanos. |
| **SDDR — Spec-Driven Development with Reports** | `__sddr` | Plano leve para uma mudança **local, pequena e bem delimitada**. |
| **AN — Analyze** | `__an` | Trilha de **diagnóstico** de um repositório existente (código, banco, APIs). *Em construção (Coming Soon)* — ainda sem template completo nem execução. |

Como decidir entre eles: ver [`04-quando-usar-ap-vs-sddr.md`](04-quando-usar-ap-vs-sddr.md).

---

## As peças de um plano

| Termo | O que é |
| --- | --- |
| **subplano (`__sp`)** | Unidade **executável** dentro de um AP. Pasta `NN-nome__sp` (com prefixo numérico de dois dígitos: `01-`, `02-`...). Seu `status.md` de raiz é a autoridade de estado. |
| **SDDD / `xx-sddd`** | A **etapa local** dentro de um subplano AP: pastas `01-sddd`, `02-sddd`... Cada etapa cobre o planejamento e a execução de uma fatia do subplano. `01-sddd` é obrigatório; `02-sddd` em diante só quando a etapa anterior não cobre o trabalho. |
| **PRD (`prd.md`)** | Definição de **produto/requisito** da etapa: Contexto, Objetivo, Escopo (o que entra / o que fica fora), Critérios de aceite. |
| **SPEC (`spec.md`)** | Definição **técnica** da etapa: Arquivos alvo, Contratos/interfaces impactados, Fluxo técnico, Validações (comandos). |
| **`dependencies.md`** | Dependências **explícitas** e bloqueios conhecidos. Obrigatório em cada `xx-sddd`. Dependência implícita é erro de método. |
| **`status.md`** | O **estado oficial** do plano/subplano. Primeira linha: `status: <estado>`. Sem `status.md` não existe execução válida. |
| **`reports/`** | **Prova de execução**, transferência de contexto e histórico técnico. É onde o resultado de fato aparece. |
| **`references/` (de um plano)** | Material de **apoio/entrada** daquele plano (amostras, prompts, contratos locais) e a gaveta `agent-audit/`. |
| **`execution-prompt.md`** | O **prompt de contexto limpo** que instrui um agente executor sobre o que ler e fazer. Neste repositório, ele vive dentro de `references/` do subplano (ver nota abaixo). |

---

## As peças exclusivas do AP

| Termo | O que é |
| --- | --- |
| **`architecting-plan/`** | Os documentos de **planejamento arquitetural** do AP: visão, escopo e módulos, dependências, execução e merge. |
| **`final-reports/`** | A **consolidação final** de todo o AP. `report-final.md` (mestre, obrigatório) + anexos + checklist do *gate* de conclusão (que autoriza mover o AP para `plans/04-completed/`). |

---

## Os estados de um `status.md`

```text
draft  →  ready  →  running  →  completed
                        ↓
                     blocked  →  abandoned
```

| Estado | Significado |
| --- | --- |
| `draft` | Em rascunho; ainda sendo planejado. |
| `ready` | Pronto para executar. |
| `running` | Execução em andamento. |
| `blocked` | Travado por dependência ou impedimento. |
| `completed` | Concluído (Definition of Done atingida). |
| `abandoned` | Abandonado; histórico imutável. |

Cada estado é também uma **subpasta** de `plans/`. O caminho feliz é numerado para ordenar
(`01-draft`, `02-ready`, `03-running`, `04-completed`); `blocked` e `abandoned` ficam sem número.
O `Status:` guarda só o nome do estado (ex.: `running`), e a subpasta correspondente é `03-running`.
Mudou o estado, move-se a pasta.

---

## O ciclo de vida (onde o plano mora)

Todo plano vive em `plans/`, na subpasta do seu status. **A subpasta corresponde ao `Status:` do
`status.md`** (caminho feliz numerado `01`–`04`; `blocked` e `abandoned` sem número) — mudou o
status, move-se a pasta.

| Subpasta | Significado |
| --- | --- |
| `plans/01-draft/` | Sendo planejado. |
| `plans/02-ready/` | Pronto para executar. |
| `plans/03-running/` | Execução ativa. |
| `plans/blocked/` | Bloqueado. |
| `plans/04-completed/` | Histórico de concluídos. |
| `plans/abandoned/` | Histórico **imutável** de abandonados. |

Só o plano de topo (AP ou SDDR) é posicionado por status; subplanos `__sp` ficam aninhados no AP.
Detalhes e regras de movimentação: [`03-estrutura-de-pastas.md`](03-estrutura-de-pastas.md).

---

## Rastreabilidade e memória

| Termo | O que é |
| --- | --- |
| **`agent-audit/`** | Gaveta de **memória operacional curta** por run. Formato de pasta: `YYYY-MM-DD__papel-do-agente__slug/` com no mínimo um `run.md`. **Handoff não vive aqui.** |
| **handoff** | A passagem de bastão. Vive em `reports/` do plano ou na resposta final do agente — nunca em `agent-audit/`. |
| **DoD (Definition of Done)** | Critérios que autorizam um plano a ir para `plans/04-completed/`: contratos cumpridos, dependências resolvidas, reports completos, `status.md = completed`. |
| **promoção para `references/`** | Mover uma verdade para o índice global só quando for repo-wide e melhor consumida fora do plano original. |

---

## Nota importante sobre `references/` no subplano

O método **canônico original** define o subplano AP apenas com `status.md` + `reports/` +
`01-sddd/`. Neste repositório, porém, adotou-se a convenção de **guardar o prompt de execução e o
material de apoio em uma pasta `references/` dentro de cada subplano**. Portanto, os subplanos aqui
têm, no mínimo:

```text
NN-nome__sp/
├── status.md
├── 01-sddd/
├── references/      ← prompt de execução + material de apoio
└── reports/
```

Este material de ajuda documenta essa convenção **como praticada**. Ver
[`05-anatomia-de-um-ap.md`](05-anatomia-de-um-ap.md).
