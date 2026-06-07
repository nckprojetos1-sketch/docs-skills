# __sddr template

## Objetivo

Template canonico para planos no caminho SDDR do metodo DOCS.

## Quando usar

- problema pequeno, local e bem delimitado
- mudanca com baixo acoplamento arquitetural
- necessidade de execucao rapida com rastreabilidade obrigatoria

## Estrutura oficial

- `status.md`
- `reports/`
- `references/agent-audit/`
- `01-sddd/`

Cada `xx-sddd/` deve conter:

- `prd.md`
- `spec.md`
- `dependencies.md`

## Regra de fronteira

- SDDR e caminho principal simples
- AP usa subplanos `__sp` com `xx-sddd`
- SDDR usa `xx-sddd` direto na raiz do plano, sem subplano `__sp`
