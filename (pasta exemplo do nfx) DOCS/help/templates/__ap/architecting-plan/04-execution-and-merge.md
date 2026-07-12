# architecting-plan · 04 — Execução e merge

## Estratégia de execução
Como os subplanos serão executados (sequência, paralelismo, quem executa cada um).

## Estratégia de merge / integração
- como o trabalho de cada subplano se integra ao todo;
- pontos de reconciliação e como conflitos serão tratados;
- cada merge relevante deve gerar um `report-merge.md` no subplano correspondente.

## Validações de integração
Comandos e checks que provam que as frentes integradas funcionam em conjunto.

- comando 1
- comando 2

## Definition of Done do AP
- [ ] todos os subplanos concluídos (`status: completed`)
- [ ] contratos entre frentes cumpridos
- [ ] dependências resolvidas
- [ ] pacote `final-reports/` completo
- [ ] decisão de conclusão e movimentação para `plans/04-completed/` registrada no `report-final.md`
