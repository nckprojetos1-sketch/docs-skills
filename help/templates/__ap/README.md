# __ap template

## Objetivo

Template canonico para AP no metodo DOCS.

AP e o caminho de planejamento e execucao para problemas grandes, estruturais e
decompostos em subplanos.

## Estrutura oficial

- `architecting-plan/`
  - documentos do planejamento arquitetural
- `01-example-subplan__sp/`
  - exemplo do formato oficial de subplano
- `final-reports/`
  - consolidacao final do AP
- `references/agent-audit/`
  - gaveta local de auditoria do AP
- `status.md`
  - estado oficial do plano

## Regra de subplano

Todo subplano de AP deve seguir esta estrutura:

- `status.md`
- `reports/`
- `01-sddd/`

Cada `01-sddd/` deve conter:

- `prd.md`
- `spec.md`
- `dependencies.md`

`02-sddd/` e seguintes surgem apenas quando necessario.

## Regra importante

- nao existe mais `backup-plans/`
- reports ficam na raiz do subplano
- `status.md` da raiz do subplano e o estado oficial
