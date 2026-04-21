# __sddr template

## Objetivo

Template canonico para planos no caminho SDDR do metodo DOCS.

## Quando usar

- problema pequeno, local e bem delimitado
- mudanca com baixo acoplamento arquitetural
- necessidade de execucao rapida com rastreabilidade obrigatoria

## Estrutura oficial

- `prd.md`
- `spec.md`
- `status.md`
- `reports/`
- `references/agent-audit/`

`dependencies.md` pode existir quando houver dependencia explicita.

## Regra de fronteira

- SDDR e caminho principal simples
- AP usa subplanos `__sp` com `xx-sddd`
- SDDR nao usa `xx-sddd`
