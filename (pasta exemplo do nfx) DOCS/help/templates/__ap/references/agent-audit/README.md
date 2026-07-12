# agent-audit

Gaveta de memória operacional curta por AP.

Use esta pasta para registrar runs de planners, executor e reviewer ligados a este AP ou aos seus
subplanos.

## Formato

- `YYYY-MM-DD__papel-do-agente__slug/`

Arquivos mínimos por run:

- `run.md`
- `artifacts/` (opcional)

## Regra

- handoff **não** fica aqui;
- handoff fica em `reports/` do plano ou subplano, ou na resposta final do agente.
