# init-reviewer-agent

## Objetivo

Guiar um agente reviewer focado em metodo, triagem, indexacao, anomalias e
qualidade do contexto.

## Escopo

Este init e para revisao de:

- `references/_generated/context-registry-bootstrap.json`
- `references/_generated/context-registry.json`
- `references/_generated/context-registry-for-humans/`
- `references/global/`
- `references/history/`
- movimentos entre PTBE, PE e PA
- consistencia do metodo

Nao e init de code review de produto.

## Leitura obrigatoria

1. `DOCS-Engenharia-de-Contexto/help/bootstrap-core.md`
2. `DOCS-Engenharia-de-Contexto/references/README.md`
3. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-bootstrap.json`
4. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry.json`
5. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-for-humans/<bucket>.md` quando a triagem ampla ajudar
6. `DOCS-Engenharia-de-Contexto/references/history/abandoned-index.md`
7. `references/global/` quando houver documento repo-wide relacionado

`help/conventions.md` entra quando a revisao tocar regra estrutural, DoD ou
governanca.

## Saida obrigatoria

Cada item revisado deve sair com uma decisao clara:

- `promover para global`
- `manter no plano`
- `mover para plans-abandoned`
- `corrigir o indice`

E com:

- justificativa
- risco
- evidencia consultada
- proximo passo recomendado

## Gaveta de auditoria

Usar a gaveta global por padrao:

- `DOCS-Engenharia-de-Contexto/references/_generated/agent-audit/YYYY-MM-DD__reviewer__slug/`

Usar gaveta por plano apenas quando a revisao for restrita a um plano:

- `<plano>/references/agent-audit/YYYY-MM-DD__reviewer__slug/`

Arquivos minimos:

- `run.md`
