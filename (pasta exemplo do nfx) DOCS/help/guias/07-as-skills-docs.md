# 07 — As skills `$docs-*`

O método DOCS é operado por um conjunto de **skills** (habilidades). Você as invoca digitando o
token `$nome-da-skill` (a `docs-init` também aceita `/docs-init`). Cada skill tem um papel claro.

> **Pré-requisito comum.** Todas as skills (exceto `$docs-pdf-context`) exigem que o repositório já
> contenha a pasta `DOCS-Engenharia-de-Contexto/`. Se ela não existir, a skill **para e encaminha
> para `$docs-init`**.

---

## Visão geral

| Skill | Papel | Executa código? |
| --- | --- | --- |
| `$docs-init` | Ponto de entrada persistente **e roteador** | não (bootstrap/validação) |
| `$docs-analyze` | **Diagnostica** quem é o dono do contexto | não |
| `$docs-plan-ap` | **Abre** um AP (planejamento) | não |
| `$docs-plan-sddr` | **Abre** um SDDR (planejamento) | não |
| `$docs-executor` | **Executa** a mudança no sistema | **sim** |
| `$docs-clean-plan-context` | **Limpa** contexto após conclusão | não (só docs) |
| `$docs-reviewer` | **Revisa** a coerência do método | não |
| `$docs-pdf-context` | Transforma um **PDF** de requisitos em contexto | não |

---

## Detalhe de cada skill

### `$docs-init` — entrada e roteamento
- **O que faz:** valida, normaliza ou cria a raiz `DOCS-Engenharia-de-Contexto/` e depois
  **encaminha** o pedido para a skill certa. É persistente — não se remove após o uso.
- **Quando usar:** ao iniciar em um repositório, quando não sabe por onde começar, ou quando outra
  skill avisa que a raiz DOCS está ausente.
- **Saída:** relatório com a ação tomada (`validated`, `normalized`, `copied-and-normalized`,
  `cloned`, `scaffolded`), a raiz do repo/DOCS, validade e avisos. **Nunca sobrescreve** arquivos
  existentes.

### `$docs-analyze` — diagnóstico de dono
- **O que faz:** encontra o plano que **já é dono** do contexto de um pedido, preferindo o dono
  mais estreito (raiz de SDDR < raiz de subplano AP < raiz de AP). Não edita, não executa, não cria
  planos.
- **Quando usar:** antes de mexer em algo, quando não está claro onde a mudança pertence.
- **Saída:** `primary_owner_path`, planos relacionados, evidências, os alvos de atualização
  (`prd`/`spec`/`reports`/`status`/`dependencies`) e uma **recomendação**: `use-existing-plan`,
  `create-sddr` ou `create-ap`. Nunca aponta para `plans/abandoned/`.

### `$docs-plan-ap` — abrir um AP
- **O que faz:** cria a estrutura de um AP (o AP + subplanos + cada `01-sddd`) e conduz uma conversa
  de planejamento. **Não executa código.**
- **Quando usar:** trabalho estrutural, multi-módulo ou multi-etapa.
- **Saída:** caminho do AP criado, subplanos criados, resumo do planejamento e o *handoff* para o
  executor. Fecha objetivo, problema, fronteiras de escopo, módulos impactados, critérios de aceite,
  sequência de subplanos, dependências e riscos.

### `$docs-plan-sddr` — abrir um SDDR
- **O que faz:** cria a estrutura de um SDDR (o SDDR + `01-sddd`) e conduz o planejamento.
  **Não executa código.**
- **Quando usar:** mudança local, pequena e bem delimitada.
- **Saída:** caminho do SDDR criado, resumo do planejamento, *handoff* e nota de atualização de
  índice. Fecha objetivo, problema, escopo, riscos/restrições, critérios de aceite, comandos de
  validação esperados e dependências explícitas.

### `$docs-executor` — executar a mudança
- **O que faz:** é a **porta principal para alterar o sistema** (ou sua documentação operacional).
  Trata o código vivo como verdade máxima e o plano/subplano/SDDD como o contrato de execução.
- **Quando usar:** implementar, corrigir, atualizar — qualquer mudança já planejada.
- **Antes de mexer, fecha:** o plano/subplano/SDDD alvo (ou confirma que é transversal), a mudança
  visível ao usuário, os arquivos/áreas tocados, as validações esperadas e quais artefatos atualizar.
- **Depois de executar, atualiza (quando aplicável):** `status.md`, `reports/`, a pasta do plano em
  `plans/<status>/` (movendo-a quando o status muda) e o `run.md` de auditoria em `references/agent-audit/`.
- **Não faz:** ler tudo de cara por padrão, super-promover para `references/`, nem colocar
  handoff em `agent-audit/`.

### `$docs-clean-plan-context` — limpar após concluir
- **O que faz:** depois que um plano é concluído, `prd.md`/`spec.md` deixam de ser o melhor ponto de
  entrada. A skill escreve um **relatório de consolidação**
  (`<alvo>/reports/report-context-consolidation.md`) com o contexto durável e então **apaga** os
  `xx-sddd/prd.md` e `xx-sddd/spec.md` já obsoletos.
- **Gates rígidos (bloqueiam a limpeza):** `status.md` ausente, status ≠ `completed`, `reports/`
  vazio, sem report de execução, PRD/SPEC ainda necessários, dependências abertas.
- **Nunca apaga:** `dependencies.md`, `status.md`, `reports/` existentes, `references/agent-audit/`,
  `architecting-plan/` nem `final-reports/`.

### `$docs-reviewer` — revisar a coerência
- **O que faz:** revisa a **coerência do método DOCS** (não é code review de produto): a curadoria
  de `references/` (contexto transversal), a estrutura de planos ativos e as movimentações entre as
  subpastas de status de `plans/`.
- **Saída:** cada item revisado termina com **uma** decisão — `promover para references`,
  `manter no plano`, `mover para plans/abandoned/` ou `corrigir o indice` — com justificativa, risco,
  evidência e próximo passo.

### `$docs-pdf-context` — PDF vira contexto
- **O que faz:** extrai um **PDF de requisitos** para um pacote de contexto compacto (não cria
  AP/SDDR/PRD/SPEC). Saída padrão em `references/<pdf-slug>/` com `README.md` + `context.json`
  + `tables.json`.
- **Quando usar:** antes de planejar, quando o requisito chegou em PDF. A saída alimenta depois o
  `$docs-plan-ap` ou o `$docs-plan-sddr`.

---

## Como as skills se encaixam no fluxo

Ver o encadeamento completo em [`08-fluxo-de-ponta-a-ponta.md`](08-fluxo-de-ponta-a-ponta.md).
