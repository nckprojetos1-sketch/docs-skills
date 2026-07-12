# Prompt — Migrar as skills `docs-*` para o modelo `plans/<status>/`

> Instrução para um **agente de contexto limpo** que vai atualizar TODAS as skills do método
> DOCS (`docs-init`, `docs-executor`, `docs-plan-ap`, `docs-plan-sddr`, `docs-analyze`,
> `docs-clean-plan-context`, `docs-reviewer`, `docs-pdf-context`). Rode este agente no
> **repositório-fonte das skills** (as cópias locais são symlink; confirme onde está o fonte
> canônico antes de editar, para não perder a mudança).

## O que mudou no método (aplique em todas as skills)

1. As três pastas de topo `plans-to-be-executed/` (PTBE), `plans-executed/` (PE) e
   `plans-abandoned/` (PA) **deixam de existir**. Passam a ser uma única `plans/` com 6 subpastas
   de status: `01-draft/`, `02-ready/`, `03-running/`, `blocked/`, `04-completed/`, `abandoned/`.
2. **Invariante:** um plano de topo vive em `plans/<status>/`, onde `<status>` == `Status:` do seu
   `status.md`. Mudou o status, move-se a pasta. Só o plano de topo é posicionado por status;
   subplanos `__sp` ficam aninhados no AP.
3. Estados oficiais passam de 5 para **6**: `draft`, `ready`, `running`, `blocked`, `completed`,
   `abandoned` (novo). Onde as skills listam os 5 estados, adicione `abandoned`.
4. **Ciclo de vida:** planos novos **nascem em `plans/01-draft/`**. Ao mudar de estado, mover a pasta
   para `plans/<novo-status>/`. Conclusão → `plans/04-completed/` (gate/DoD inalterado; AP ainda exige
   `final-reports/` completo). Abandono → `plans/abandoned/` (imutável; retomar exige novo plano em
   `plans/01-draft/`).
5. **`references/`:** pastas-padrão passam a ser `agent-audit/`, `api-documentations/`,
   `build-documentation/`, `database-documentation/`, `execution-references/`, `prompts/`. Não há
   mais `global/`, `history/`, `abandoned-index` nem a gaveta `references/_generated/agent-audit/`
   (a gaveta global agora é `references/agent-audit/`).
6. **Abreviações PTBE/PE/PA** saem do vocabulário.

## Decisão explícita a tomar: o `context-registry` / `_generated`

O novo modelo **não exige** o índice gerado (`references/_generated/context-registry*.json` +
`context-registry-for-humans/`). Escolha uma das duas linhas e aplique de forma coerente em todas
as skills e scripts:

- **(Recomendado) Aposentar** o mecanismo: remova `_generated`/`context-registry` do contrato
  obrigatório e do fluxo de descoberta; a descoberta passa a começar pelas pastas-domínio de
  `references/` + o plano em `plans/<status>/`. **OU**
- **Manter como índice opcional**: se preferir manter o registro, gere-o dentro de `references/`
  como apoio opcional (nunca obrigatório) e ajuste a validação para não falhar quando ele não existir.

## Inventário de alvos (edite todos)

### SKILL.md (8 arquivos)
Substitua nomes de pasta, abreviações e vocabulário de status em cada `SKILL.md`. Pontos conhecidos:
- `docs-init/SKILL.md`: lista de "Minimum DOCS root entries" com `plans-to-be-executed`,
  `plans-executed`, `plans-abandoned` → `plans/` com as 6 subpastas; contrato de `references/`
  (`_generated/...`) conforme a decisão acima.
- `docs-executor/SKILL.md`: pós-execução deve mover a pasta do plano quando o status muda;
  referências a `references/_generated/...`, `references/history/abandoned-index.md`,
  `references/global/` → novo modelo.
- `docs-plan-ap/SKILL.md` e `docs-plan-sddr/SKILL.md`: "criar em `plans-to-be-executed/`" →
  "criar em `plans/01-draft/`".
- `docs-analyze/SKILL.md`: candidatos de dono passam a ser as subpastas de `plans/`
  (`plans/01-draft|ready|running|blocked|completed/`); `plans/abandoned/` = evidência histórica,
  nunca dono mutável.
- `docs-reviewer/SKILL.md`: descrição e decisões — "movimentos PTBE/PE/PA" → "movimentos entre as
  subpastas de status de `plans/`"; decisão `mover para plans-abandoned` → `mover para plans/abandoned/`.
- `docs-clean-plan-context/SKILL.md`: mantém o gate em `status == completed`; ajuste apenas
  referências a `_generated`/subpastas antigas.
- `docs-pdf-context/SKILL.md`: escreve em `references/global/<slug>/` → escolha uma pasta-domínio
  adequada (ex.: `references/<dominio>/` ou uma nova pasta de contexto) coerente com o novo modelo.

### `docs-method-core.md` (núcleo compartilhado — 6 cópias)
Presente em `docs-init`, `docs-executor`, `docs-plan-ap`, `docs-plan-sddr`, `docs-reviewer`
(idêntico) e em `docs-analyze` (variante). Atualize em todas:
- "Official Roots": trocar as três pastas de ciclo de vida por `plans/` + as 6 subpastas.
- "Official statuses: draft, ready, running, blocked, completed" → adicionar `abandoned`.
- DoD: destino da conclusão passa a ser `plans/04-completed/`.

### Scripts Python (criam/validam a estrutura)
- `docs-init/scripts/common.py`: `REQUIRED_DOCS_ENTRIES` — trocar `plans-to-be-executed`,
  `plans-executed`, `plans-abandoned` por `plans` (e, se quiser validar as subpastas, exigir
  `plans/01-draft`, `.../ready`, `.../running`, `.../blocked`, `.../completed`, `.../abandoned`).
  Ajustar/remover `REQUIRED_GENERATED_ENTRIES` conforme a decisão do registry.
- `docs-init/scripts/docs_init.py`: o README template, o texto de `CONVENTIONS` (estados oficiais →
  6; regra de estrutura → `plans/<status>/`) e a lista de `mkdir` em `normalize_docs()` — criar
  `plans/` + as 6 subpastas e as 6 pastas-padrão de `references/` (não mais `global/`, `history/`,
  `_generated/`).
- `docs-plan-ap/scripts/create_ap.py`: `plans_root = docs_root / "plans-to-be-executed"` →
  `docs_root / "plans" / "draft"`. Mantém `status: draft` no `status.md` criado (o plano nasce draft).
- `docs-plan-sddr/scripts/create_sddr.py`: idem — criar em `plans/01-draft/`.

### Scaffold `docs-init/assets/DOCS-Engenharia-de-Contexto/`
É o pacote que a `docs-init` copia para novos repositórios. Ele está na versão ANTIGA. Substitua-o
pela versão nova do método: use como fonte o `help/` já atualizado em
`c:\Repositorios\NFX-Rebootado\DOCS-Engenharia-de-Contexto`, que passou a ser **guias + templates**
(`README.md` + `help/guias/` + `help/templates/`; a camada normativa foi consolidada nos guias, em
especial `09-convencoes.md`), mais o `references/` de 6 pastas. Garanta que o scaffold crie `plans/`
com as 6 subpastas — `01-draft/`, `02-ready/`, `03-running/`, `04-completed/`, `blocked/`,
`abandoned/` (com `.gitkeep`) — e não mais as três pastas antigas.

### Contratos de init
> O `help/` do método foi consolidado em **guias + templates** (sem `inits/` como pasta separada; as
> regras de entrada agora vivem nos guias). Ao migrar as skills, decida se mantém os init-agents nas
> skills alinhados ao novo modelo ou se dobra suas regras nos guias / `docs-method-core.md`. Se
> mantiver, aplique:
- `init-plan-ap-agent.md` / `init-plan-sddr-agent.md`: plano nasce em `plans/01-draft/`.
- `init-reviewer-agent.md`: revisa movimentos entre subpastas de status; decisão `mover para plans/abandoned/`.
- `init-executor-agent.md`: sem `abandoned-index`; abandono = mover para `plans/abandoned/`.

### Templates de gate no scaffold
`assets/.../help/templates/__ap/final-reports/`: "Gate estrito PTBE -> PE" → "Gate de conclusão
(mover o AP para `plans/04-completed/`)"; "Decisão de migração PTBE → PE" → "Decisão de conclusão e
movimentação para `plans/04-completed/`". Os `status.md` template mantêm `status: draft`.

## Verificação final (checklist)

1. `grep -ri "plans-to-be-executed\|plans-executed\|plans-abandoned\|PTBE\|PE\b\|PA\b"` em todas as
   skills e no scaffold → **zero** ocorrências (fora de exemplos que narrem explicitamente o modelo
   antigo para contraste).
2. Os scripts criam `plans/` + 6 subpastas e as 6 pastas-padrão de `references/`; `create_ap.py` e
   `create_sddr.py` criam em `plans/01-draft/`.
3. `common.py` valida `plans/` (não as três pastas antigas); a validação do registry está coerente
   com a decisão tomada.
4. `docs-method-core.md` (todas as cópias) lista 6 estados e o modelo `plans/<status>/`.
5. Rodar `docs-init` em um repositório de teste produz a estrutura nova, íntegra, e as skills
   `docs-plan-ap`/`docs-plan-sddr` criam planos em `plans/01-draft/`.
6. `docs-reviewer` e `docs-analyze` referem-se somente às subpastas de status de `plans/`.

## Observação

Este prompt altera **apenas as skills e seu scaffold**. A migração da estrutura de um repositório
já existente é feita pelo prompt companheiro
`2026-07-11__migrar-estrutura-docs-para-plans-status.md`.
