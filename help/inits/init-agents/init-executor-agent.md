# init-executor-agent

## Objetivo

Ser a porta principal para qualquer agente que vai alterar o sistema ou a
documentacao operacional ligada ao sistema.

Este init carrega o contexto operacional do metodo DOCS e define como o
executor deve agir dentro dele.

## Quando usar

- implementacao de codigo
- atualizacao de planos ativos
- manutencao do metodo DOCS
- correcao de runtime com impacto em documentacao

## Modelo mental do executor

O executor deve operar com estas regras na cabeca:

- codigo vivo é a verdade maxima;
- plano, subplano ou etapa relevante vem logo depois;
- `references/` existe para apontar o melhor caminho de leitura, nao para
  substituir o plano;
- historico serve como evidencia e apoio, nao como contexto vivo por padrao;
- bootstrap deve ser barato e dirigido.

## Leitura minima obrigatoria

Antes de executar, leia:

1. este arquivo inteiro;
2. `DOCS-Engenharia-de-Contexto/help/bootstrap-core.md`;
3. `DOCS-Engenharia-de-Contexto/references/README.md`;
4. `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-bootstrap.json`.

Abrir somente se necessario:

- `DOCS-Engenharia-de-Contexto/references/_generated/context-registry.json`
  quando faltarem sinais;
- `DOCS-Engenharia-de-Contexto/references/_generated/context-registry-for-humans/<bucket>.md`
  quando a busca ainda estiver ampla;
- `DOCS-Engenharia-de-Contexto/help/conventions.md` quando houver duvida
  estrutural, governanca, DoD ou conflito de metodo;
- `DOCS-Engenharia-de-Contexto/README.md` quando precisar de visao geral curta do
  pacote DOCS.

## Fluxo oficial de descoberta

1. entrar por `references/_generated/context-registry-bootstrap.json`;
2. localizar o tema;
3. abrir `best_entry_path`;
4. abrir `context-registry.json` completo somente se faltarem sinais;
5. abrir o bucket humano somente se a triagem ainda estiver ampla;
6. abrir codigo correlato.

Nunca comece pelo registry completo por padrao.

## Quando existe plano alvo

Se a execucao estiver vinculada a um plano, ler tambem:

1. `<plano>/status.md`;
2. SDDR raiz ou `xx-sddd/` pertinente;
3. `reports/` do plano ou subplano quando precisar de evidencia ou handoff.

Regras:

- atualizar `status.md` quando o estado real mudar;
- atualizar `reports/` quando a execucao gerar evidencia, handoff ou merge
  relevante;
- tratar plano historico apenas como evidencia ou contrato suplementar.

## O que atualizar apos a execucao

Sempre avaliar se houve mudanca em:

- indexacao do tema;
- status do plano, subplano ou etapa;
- valor residual historico;
- verdade repo-wide.

Atualizar somente quando aplicavel:

- `references/_generated/context-registry-bootstrap.json`
- `references/_generated/context-registry.json`
- `references/_generated/context-registry-for-humans/`
- `references/history/abandoned-index.md`
- `references/global/`

## O que o executor nao deve fazer

- nao ler o registry completo por padrao;
- nao promover para `references/` o que continua melhor explicado no plano,
  subplano ou codigo;
- nao tratar historico como contexto vivo por default;
- nao gravar handoff em `agent-audit/`.

## Gaveta de auditoria

- usar gaveta por plano quando a execucao estiver vinculada a um plano:
  - `<plano>/references/agent-audit/YYYY-MM-DD__executor__slug/`
- usar gaveta global quando a execucao for transversal ao metodo:
  - `DOCS-Engenharia-de-Contexto/references/_generated/agent-audit/YYYY-MM-DD__executor__slug/`

Arquivos minimos:

- `run.md`

## Checklist de saida

- codigo e validacoes concluidos;
- `status.md` atualizado quando aplicavel;
- `reports/` atualizados quando aplicavel;
- indices atualizados quando a navegacao do tema mudou;
- `history/` atualizado quando houve abandono com valor;
- `global/` atualizado quando houve nova verdade repo-wide;
- auditoria preenchida quando fizer sentido.
