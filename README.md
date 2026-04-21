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
|-- plans-to-be-executed/
|-- plans-executed/
`-- plans-abandoned/
```

Camadas oficiais:

1. `help/`
   - metodo, regras, inits e templates
2. `references/`
   - indice curto e poucas verdades globais
3. `plans-to-be-executed/`
   - execucao ativa e mutavel
4. `plans-executed/` e `plans-abandoned/`
   - historico

Hierarquia oficial de verdade:

1. codigo vivo do repositorio
2. planos e subplanos relevantes
3. `references/` como indice e apoio global
4. historico restante

## Entrada recomendada

Entre por intencao:

- alterar o sistema:
  `help/inits/init-agents/init-executor-agent.md`
- abrir AP:
  `help/inits/init-agents/init-plan-ap-agent.md`
- abrir SDDR:
  `help/inits/init-agents/init-plan-sddr-agent.md`
- revisar coerencia do metodo:
  `help/inits/init-agents/init-reviewer-agent.md`
- consultar regra estrutural:
  `help/conventions.md`
- entender o metodo em leitura curta:
  `help/bootstrap-core.md`

## Skills operacionais

Este repositorio tambem empacota o metodo como skills para agentes.

Instale ou atualize todas com:

```powershell
python .\scripts\install_docs_skills.py
```

Comandos instalados:

- `$docs-init`
- `$docs-executor`
- `$docs-plan-ap`
- `$docs-plan-sddr`
- `$docs-reviewer`

As skills antigas `xml-docs-init-*` sao desativadas pelo instalador somente
depois que as novas skills forem copiadas e validadas.

## Pasta `references/`

`references/` nao existe para substituir subplanos, SDDDs ou SDDRs.

Ela existe para:

- dizer para o agente onde buscar;
- indexar o que ja foi executado;
- guardar poucas verdades globais que nao pertencem a um unico plano.

Estrutura oficial:

```text
references/
|-- README.md
|-- global/
|-- history/
`-- _generated/
```

Indices oficiais:

- `references/_generated/context-registry-bootstrap.json`
- `references/_generated/context-registry.json`
- `references/_generated/context-registry-for-humans/`

Fluxo recomendado de descoberta:

1. `references/README.md`
2. `references/_generated/context-registry-bootstrap.json`
3. `best_entry_path` do tema
4. `references/_generated/context-registry.json` somente se faltar sinal
5. `references/_generated/context-registry-for-humans/<bucket>.md` somente se a busca ainda estiver ampla
6. plano, subplano ou `xx-sddd` relevante
7. codigo correlato

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

- global: `references/_generated/agent-audit/`
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
`references/` aponta.
`plans-*` guardam o contexto real.
`codigo` continua sendo a verdade maxima.
