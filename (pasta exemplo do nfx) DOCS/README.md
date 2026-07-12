# DOCS - Engenharia de Contexto

Documentacao oficial do metodo.

## Visao geral

DOCS e um metodo de engenharia de contexto para trabalho orientado por IA.

Ele existe para:

- externalizar memoria;
- dar rastreabilidade a decisoes;
- separar indice de contexto e historico bruto;
- tornar execucao, revisao e handoff previsiveis.

Documentacao, aqui, nao e subproduto. Ela e infraestrutura operacional.

## Estrutura oficial

```text
DOCS-Engenharia-de-Contexto/
|-- README.md
|-- help/
|-- references/
`-- plans/
    |-- 01-draft/
    |-- 02-ready/
    |-- 03-running/
    |-- blocked/
    |-- 04-completed/
    `-- abandoned/
```

Camadas oficiais:

1. `help/`
   - o metodo: guias (`guias/`) e templates (`templates/`)
2. `references/`
   - contexto transversal do projeto (verdades globais e documentacao viva)
3. `plans/`
   - todos os planos, organizados por status

Hierarquia oficial de verdade:

1. codigo vivo do repositorio
2. planos e subplanos relevantes
3. `references/` como indice e apoio global
4. historico restante

## A pasta `plans/`

Todos os planos (AP ou SDDR) vivem em `plans/`, dentro de uma subpasta que corresponde
ao seu status.

Estados oficiais e subpastas:

| status | significado | subpasta |
| --- | --- | --- |
| `draft` | sendo planejado | `plans/01-draft/` |
| `ready` | pronto para executar | `plans/02-ready/` |
| `running` | execucao em andamento | `plans/03-running/` |
| `blocked` | bloqueado por dependencia ou impedimento | `plans/blocked/` |
| `completed` | executado com sucesso (DoD atingida) | `plans/04-completed/` |
| `abandoned` | abandonado; historico imutavel | `plans/abandoned/` |

Ordenacao: as quatro etapas do caminho feliz recebem prefixo numerico para ordenar
(`01-draft`, `02-ready`, `03-running`, `04-completed`); `blocked` e `abandoned` ficam sem
prefixo. O `Status:` guarda so o nome do estado (ex.: `running`); a subpasta e `03-running`.

Regra central (invariante): o `Status:` do `status.md` e a subpasta correspondente nunca
divergem. Quando o status muda, a **pasta do plano e movida** para a subpasta correspondente.
Nao existe mais `plans-to-be-executed/`, `plans-executed/` nem `plans-abandoned/`.

Apenas o plano de topo (AP ou SDDR) e posicionado por status. Os subplanos `__sp` ficam
aninhados dentro do AP e nao sao movidos para subpastas de status; o `status.md` da raiz
do plano de topo determina a subpasta.

## Pasta `references/`

`references/` nao existe para substituir subplanos, SDDDs ou SDDRs.

Ela existe para guardar o contexto transversal do projeto: verdades globais e
documentacao viva que vale para varios planos e deve permanecer atualizada.

Pastas-padrao:

```text
references/
|-- agent-audit/            # gaveta global de runs de agente
|-- api-documentations/     # contratos e documentacao de APIs (manter atualizada)
|-- build-documentation/    # build, deploy, Docker/compose, runtime (manter atualizada)
|-- database-documentation/ # schema, indices, consultas, tuning (manter atualizada)
|-- execution-references/   # referencias transversais de execucao
`-- prompts/                # prompts reutilizaveis (inclui prompts de migracao do metodo)
```

Pastas especificas de um projeto (ex.: `IMPORTANTE/`) sao permitidas alem das padrao.

Fluxo recomendado de descoberta (afunilar do indice ao codigo):

1. `references/README.md` e as pastas-dominio relevantes
   (`database-documentation/`, `api-documentations/`, `build-documentation/`)
2. o plano relevante em `plans/<status>/` (seu `status.md`, `reports/`, `xx-sddd/`)
3. codigo correlato

## Caminhos de trabalho

### AP - Architecting Plan

Usar AP quando:

- houver impacto arquitetural;
- existir decomposicao em subplanos;
- mais de um modulo ou frente precisarem ser coordenados.

Estrutura base do AP:

- `architecting-plan/`
- subplanos `NN-nome__sp/`
- `final-reports/`
- `references/agent-audit/`
- `status.md`

### SDDR - Spec-Driven Development with Reports

Usar SDDR quando a mudanca for local, pequena ou bem delimitada.

Fluxo base:

1. `prd.md`
2. `spec.md`
3. execucao
4. `reports/`
5. `status.md`

### SDDD dentro de subplanos AP

Subplanos de AP seguem o modelo:

```text
NN-nome__sp/
|-- status.md
|-- reports/
`-- 01-sddd/
    |-- prd.md
    |-- spec.md
    `-- dependencies.md
```

Regras:

- todo subplano deve nascer com `01-sddd/`;
- `02-sddd/`, `03-sddd/` e seguintes surgem apenas quando necessario;
- `status.md` da raiz do subplano e o estado oficial;
- `reports/` da raiz do subplano consolida execucao e handoffs;
- cada `xx-sddd/` cobre o planejamento e a execucao local daquela etapa.

## Auditoria operacional

Gavetas oficiais de auditoria de agente:

- global: `references/agent-audit/`
- por plano: `<plano>/references/agent-audit/`

Formato canonico:

- `YYYY-MM-DD__agent-role__slug/`

Arquivos minimos:

- `run.md`
- `artifacts/` opcional

Regra:

- handoff nao vive em `agent-audit/`
- handoff vive em `reports/` do plano ou na resposta final do agente

## Conclusao

DOCS organiza como agentes planejam, executam, revisam e entregam contexto.

`help/` define o metodo.
`references/` aponta e centraliza contexto global.
`plans/` guarda o contexto real, organizado por status.
`codigo` continua sendo a verdade maxima.
