# agent-audit (global)

Gaveta **global** de memória operacional curta: runs de agente que não pertencem a um
único plano — reviews do método, migrações, auditorias transversais.

Cada plano/subplano mantém a sua própria `references/agent-audit/`; esta é a gaveta
**repo-wide**.

## Formato

- `YYYY-MM-DD__agent-role__slug/`

Arquivos mínimos por run:

- `run.md`
- `artifacts/` opcional

## Regra

- handoff não fica aqui;
- handoff fica em `reports/` do plano ou na resposta final do agente.
