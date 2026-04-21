# init-plan-ap-agent

## Objetivo

Guiar um agente planner que vai abrir um novo AP.

Este init existe para criar a estrutura do plano e conduzir uma conversa focada
em ideia, escopo, fronteiras e decomposicao, sem executar codigo.

## Quando usar

- problema arquitetural
- mais de um modulo ou frente
- necessidade de decompor em subplanos
- necessidade de handoff claro para executor posterior

## Leitura obrigatoria

1. `DOCS-Engenharia-de-Contexto/help/bootstrap-core.md`
2. `DOCS-Engenharia-de-Contexto/references/README.md`
3. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-bootstrap.json`
4. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry.json` somente se o bootstrap fino nao bastar
5. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-for-humans/<bucket>.md` somente se a busca ainda estiver ampla
6. `DOCS-Engenharia-de-Contexto/references/history/abandoned-index.md` quando o tema tocar descarte ou retomada

`help/conventions.md` entra so quando houver duvida estrutural ou conflito de metodo.
`DOCS-Engenharia-de-Contexto/README.md` entra somente como visao geral opcional.

## Conversa que este agente deve conduzir

O agente planner AP deve fechar:

- objetivo do plano
- motivacao e problema
- fronteiras de escopo
- modulos ou areas impactadas
- criterios de aceite
- decomposicao em subplanos

O agente nao deve aprofundar implementacao alem do necessario para a abertura do
AP.

## Entrega estrutural obrigatoria

Ao abrir o AP, o planner deve criar:

- pasta do AP em `plans-to-be-executed/`
- `status.md` do AP
- `architecting-plan/`
- `final-reports/`
- `references/agent-audit/`
- subplanos `NN-...__sp/`

Em cada subplano criado, deve gerar:

- `status.md`
- `reports/`
- `01-sddd/`

Em cada `01-sddd/`, deve gerar:

- `prd.md`
- `spec.md`
- `dependencies.md`

## Limite do planner

O planner AP para em planejamento leve:

- estrutura criada
- escopo definido
- PRD e SPEC iniciais escritos
- subplanos e `01-sddd/` criados

Ele nao:

- executa codigo
- emite report de execucao
- detalha implementacao profundamente

## Atualizacao de references

Ao final, o planner deve avaliar se o novo AP muda a indexacao do tema.

Se sim, ele deve atualizar:

- `references/_generated/context-registry-bootstrap.json`
- `references/_generated/context-registry.json`
- `references/_generated/context-registry-for-humans/`

Somente quando o AP criar uma verdade repo-wide, ele tambem atualiza:

- `references/global/`

## Gaveta de auditoria

Registrar a run na gaveta do plano:

- `<plano>/references/agent-audit/YYYY-MM-DD__planner-ap__slug/`

Arquivos minimos:

- `run.md`


