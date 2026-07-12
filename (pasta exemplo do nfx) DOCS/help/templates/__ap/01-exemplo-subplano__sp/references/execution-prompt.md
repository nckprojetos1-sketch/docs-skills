# Execution Prompt — Subplano NN — <nome do subplano>

Use este prompt em uma sessão de **contexto limpo** para executar este subplano.

## Prompt

Você é o executor do subplano `NN-<slug>__sp` do AP `<nome>__ap`.

Trabalhe no repositório:

```text
<caminho absoluto do repositório>
```

## Leitura obrigatória

Antes de alterar qualquer arquivo, leia, nesta ordem:

1. `DOCS-Engenharia-de-Contexto/plans/<status>/<nome>__ap/architecting-plan/01-vision.md`;
2. `.../architecting-plan/02-scope-and-modules.md`;
3. `.../architecting-plan/03-dependencies.md`;
4. `.../NN-<slug>__sp/status.md`;
5. `.../NN-<slug>__sp/01-sddd/prd.md`;
6. `.../NN-<slug>__sp/01-sddd/spec.md`;
7. `.../NN-<slug>__sp/01-sddd/dependencies.md`;
8. arquivos-chave do repositório relevantes a esta etapa.

## Estado inicial esperado

Descreva o que o repositório **já** deve ter antes deste subplano e o que **ainda não** deve ter.
Se encontrar diferença relevante, adapte a execução preservando a intenção do subplano e registre
no report.

## Decisões travadas

Liste as decisões que o executor **não pode violar** sem parar e registrar um conflito
(ex.: stack, banco canônico, o que não usar).

## Objetivo da execução

O resultado concreto que esta execução deve produzir.

## Bloqueios de arquitetura

Interrompa e registre conflito se a execução exigir algo que contrarie as decisões travadas do AP.

## Report obrigatório

Ao final, crie um report em `.../NN-<slug>__sp/reports/AAAA-MM-DD__execution-report.md` contendo:
resumo do que foi implementado, arquivos alterados, comandos/validações executados, saída resumida,
falhas/bloqueios e pendências para o próximo subplano.
