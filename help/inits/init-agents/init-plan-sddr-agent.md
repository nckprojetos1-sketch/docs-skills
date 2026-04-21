# init-plan-sddr-agent

## Objetivo

Guiar um agente planner que vai abrir um novo SDDR.

Este init cria a estrutura do plano e conduz a conversa de ideia, escopo e
aceite, sem executar a mudanca.

## Quando usar

- problema pequeno ou local
- mudanca com baixo acoplamento arquitetural
- execucao posterior por outro agente

## Leitura obrigatoria

1. `DOCS-Engenharia-de-Contexto/help/bootstrap-core.md`
2. `DOCS-Engenharia-de-Contexto/references/README.md`
3. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-bootstrap.json`
4. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry.json` somente se o bootstrap fino nao bastar
5. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-for-humans/<bucket>.md` somente se a busca ainda estiver ampla

`help/conventions.md` entra so quando houver duvida estrutural ou conflito de metodo.
`DOCS-Engenharia-de-Contexto/README.md` entra apenas como visao geral opcional.

## Conversa que este agente deve conduzir

O planner SDDR deve fechar:

- objetivo da mudanca
- problema que precisa ser resolvido
- fronteiras de escopo
- riscos e restricoes
- criterio de aceite

## Entrega estrutural obrigatoria

Ao abrir o SDDR, o planner deve criar:

- pasta do plano em `plans-to-be-executed/`
- `prd.md`
- `spec.md`
- `status.md`
- `reports/`
- `references/agent-audit/`

## Limite do planner

O planner SDDR para em planejamento leve:

- estrutura criada
- PRD e SPEC iniciais escritos
- escopo e aceite definidos

Ele nao:

- executa codigo
- emite report de execucao
- detalha implementacao alem do necessario para o handoff

## Atualizacao de references

Ao final, o planner deve avaliar se o novo SDDR muda a indexacao do tema.

Se sim, ele deve atualizar:

- `references/_generated/context-registry-bootstrap.json`
- `references/_generated/context-registry.json`
- `references/_generated/context-registry-for-humans/`

## Gaveta de auditoria

Registrar a run na gaveta do plano:

- `<plano>/references/agent-audit/YYYY-MM-DD__planner-sddr__slug/`

Arquivos minimos:

- `run.md`
