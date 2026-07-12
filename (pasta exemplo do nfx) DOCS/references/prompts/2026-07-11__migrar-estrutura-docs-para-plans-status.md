# Prompt — Migrar a estrutura DOCS para o modelo `plans/<status>/`

> Instrução para um **agente de contexto limpo** trabalhando dentro de um repositório que
> já usa o método DOCS na versão antiga (com `plans-to-be-executed/`, `plans-executed/` e
> `plans-abandoned/`). Copie este texto inteiro como prompt inicial do agente.

## Objetivo

Adaptar a **estrutura** e a **documentação local** deste repositório à nova versão do método
DOCS, sem perder nem apagar nenhum plano ou contexto. Os planos são apenas **reposicionados**.

## Precondição (o humano já fez)

A pasta nova `help/` do método (guias + templates) já foi copiada para
`DOCS-Engenharia-de-Contexto/`. Ela é a **fonte da verdade** do novo modelo. **Não** a
altere para o modelo antigo; ao contrário, use-a para guiar esta migração.

## O que mudou (leia `help/` antes de agir)

1. As três pastas de topo `plans-to-be-executed/` (PTBE), `plans-executed/` (PE) e
   `plans-abandoned/` (PA) **deixam de existir**. Passam a ser uma única pasta `plans/` com
   **6 subpastas de status**: `01-draft/`, `02-ready/`, `03-running/`, `blocked/`, `04-completed/`,
   `abandoned/`.
2. **Invariante:** um plano de topo (AP ou SDDR) vive em `plans/<status>/`, onde `<status>` é
   idêntico ao campo `Status:` do seu `status.md`. Mudou o status, move-se a pasta. Só o plano
   de topo é posicionado por status; subplanos `__sp` ficam **aninhados** no AP.
3. Estados oficiais (6): `draft`, `ready`, `running`, `blocked`, `completed`, `abandoned`.
4. `references/` guarda contexto transversal. Pastas-padrão: `agent-audit/`,
   `api-documentations/`, `build-documentation/`, `database-documentation/`,
   `execution-references/`, `prompts/`. Não há mais `global/`, `history/`, `_generated/`,
   `context-registry` nem `abandoned-index`. A gaveta global de auditoria é
   `references/agent-audit/`.

## Passos

### 0. Preparação
- Leia os guias em `help/guias/` (a referência normativa de regras é `help/guias/09-convencoes.md`).
- Confirme que está em um repositório git. **Toda movimentação de plano usa `git mv`** (preserva
  histórico). **Nunca** use delete/rm em conteúdo de plano.

### 1. Inventário
- Liste todos os planos de topo em `plans-to-be-executed/`, `plans-executed/` e
  `plans-abandoned/` (pastas terminadas em `__ap` ou `__sddr`).
- Para cada um, leia o `status.md` e anote o valor atual de `Status:`.

### 2. Criar `plans/`
- Crie `plans/` com as 6 subpastas de status, cada uma com um `.gitkeep`. As quatro etapas do
  caminho feliz têm prefixo numérico para ordenar; `blocked` e `abandoned` ficam sem prefixo:

  | status | subpasta |
  | --- | --- |
  | `draft` | `plans/01-draft/` |
  | `ready` | `plans/02-ready/` |
  | `running` | `plans/03-running/` |
  | `completed` | `plans/04-completed/` |
  | `blocked` | `plans/blocked/` |
  | `abandoned` | `plans/abandoned/` |

### 3. Reposicionar cada plano de topo
Para cada plano, mapeie o `Status:` atual para um dos 6 canônicos e mova a pasta para a subpasta
correspondente (tabela acima):

`git mv <pasta-antiga>/<plano> plans/<subpasta-do-status>/<plano>`

**Tabela de mapeamento** (status legado livre → canônico). Sempre escolha o estado que melhor
reflete a **realidade** do plano:

| status legado (exemplos) | canônico |
| --- | --- |
| `draft`, `rascunho` | `draft` |
| `ready`, `code-ready`, `execution-ready` | `ready` |
| `running`, `in-progress`, `implementation-in-progress` | `running` |
| `blocked`, qualquer `*-blocked` | `blocked` |
| `executed`, `completed`, `done`, `completed-with-known-limits` | `completed` |
| `abandoned` (ou plano vindo de `plans-abandoned/`) | `abandoned` |

Casos de julgamento:
- **AP com subplanos em estados mistos** (ex.: `Status: subplans-documented`): o AP como um todo
  costuma estar em `running` se há subplanos em execução/concluídos, ou `ready` se nada começou.
  Decida pela realidade agregada.
- Planos que estavam em `plans-abandoned/` vão para `plans/abandoned/` com `Status: abandoned`.
- Planos que estavam em `plans-executed/` normalmente viram `completed`.

### 4. Normalizar os `status.md`
- Em **todo** `status.md` (planos de topo **e** subplanos), troque o token de `Status:` por um dos
  6 canônicos.
- **Preserve toda a nuance**: se o valor antigo carregava detalhe (ex.: `completed-with-known-limits`),
  mantenha esse detalhe na linha `Execution status:` ou no corpo. Não apague informação.

### 5. Remover as pastas antigas
- Depois de mover tudo, remova `plans-to-be-executed/`, `plans-executed/` e `plans-abandoned/`
  (que agora só devem conter `.gitkeep`). Use `git rm` no `.gitkeep` e apague os diretórios vazios.
- Confirme com `git status` que **não há deleções de conteúdo real** — apenas renomeações.

### 6. Padronizar `references/`
- Garanta as 6 pastas-padrão. Crie as que faltarem, cada uma com um `README.md` curto explicando
  seu propósito e (para database/api/build) a regra de "manter atualizada".
- **Preserve** pastas específicas do projeto (ex.: `IMPORTANTE/`) e seu conteúdo.
- Se existirem `global/`, `history/` ou `_generated/` com conteúdo real, não apague: mova o
  conteúdo útil para a pasta-domínio adequada e registre a decisão; se estiverem vazias, remova-as.

### 7. Corrigir paths de navegação vivos
- Nos arquivos **vivos** (não-históricos) que referenciam caminhos antigos, troque o prefixo
  `plans-to-be-executed/<plano>` (ou `plans-executed/`, `plans-abandoned/`) por
  `plans/<status>/<plano>`. Arquivos vivos incluem: `status.md`, `execution-prompt.md`, os `xx-sddd/`
  (`prd.md`, `spec.md`, `dependencies.md`), índices de `architecting-plan/`, e material de apoio em
  `references/` do plano.
- **Preserve verbatim** o histórico: nada em `/reports/`, `/final-reports/` ou `/agent-audit/` deve
  ter paths reescritos — são registros do que aconteceu.
- Atenção a paths com separador Windows (`\`) além de `/`.

### 8. Documentação local
- Atualize qualquer documentação **do projeto** (fora de `help/`, que já vem
  prontas) que ainda descreva as pastas antigas, o registry ou o `abandoned-index`.

## Verificação final (checklist)

1. `grep -ri "plans-to-be-executed\|plans-executed\|plans-abandoned\|PTBE\|_generated\|abandoned-index"`
   fora de `/reports/`, `/final-reports/`, `/agent-audit/` → **zero** ocorrências.
2. `plans/` tem as 6 subpastas; cada plano de topo está na subpasta igual ao seu `Status:`.
3. Invariante conferido: para cada plano de topo, `status.md → Status:` == nome da subpasta.
4. `references/` tem as 6 pastas-padrão (todas com README); pastas do projeto preservadas.
5. `git status` / `git log --follow` mostram os planos **movidos** (histórico preservado),
   nada de conteúdo deletado; `reports/` históricos inalterados.
6. As três pastas antigas não existem mais.

## Garantia inviolável

Nenhum plano nem contexto pode ser perdido ou apagado. Planos apenas mudam de lugar; relatórios e
auditorias históricas ficam verbatim.
