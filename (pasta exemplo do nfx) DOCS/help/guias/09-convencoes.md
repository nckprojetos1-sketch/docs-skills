# 09 — Convenções canônicas (referência)

Este é o resumo **normativo** das regras do método — a referência canônica de regras, com acentuação
e reconciliada com a prática atual do repositório.

> **Estas regras são normativas, não opcionais, e valem para pessoas e agentes.**

---

## Nomenclatura

**Pastas:** sempre minúsculas, `kebab-case`, sem espaços, sem acentos.
**Exceção:** a pasta raiz pode se chamar `DOCS-Engenharia-de-Contexto`.

**Sufixos oficiais:** `__ap`, `__sddr`, `__sp` (e `__an`, ainda em construção).

- AP: `<slug>__ap`
- Subplano: `NN-<slug>__sp` (prefixo numérico de dois dígitos: `01-`, `02-`...)
- SDDR: `<slug>__sddr`

**Etapas internas de subplano:** `01-sddd`, `02-sddd`, `03-sddd`... (`01-sddd` obrigatório;
`02-sddd` nunca antes de `01-sddd`).

**Pastas de auditoria (run):** `YYYY-MM-DD__papel-do-agente__slug/` — ex.:
`2026-07-08__executor__slug`, `__planner-ap__`, `__planner-sddr__`, `__reviewer__`,
`__clean-plan-context__`.

---

## Arquivos canônicos por tipo de plano

**AP (raiz):**
```text
architecting-plan/  ·  final-reports/  ·  status.md  ·  references/agent-audit/  ·  subplanos NN-...__sp/
```

**Subplano AP (`__sp`)** — *convenção deste repositório:*
```text
status.md  ·  01-sddd/  ·  references/  ·  reports/
```
> O `01-sddd/` traz `prd.md` + `spec.md` + `dependencies.md`. O **prompt de execução** vive em
> `references/execution-prompt.md`. (O método canônico original define o subplano só com `status.md`
> + `reports/` + `01-sddd/`; aqui adotou-se `references/` para o prompt e o material de apoio.)

**SDDR (raiz):**
```text
status.md  ·  01-sddd/  ·  references/agent-audit/  ·  reports/
```
> `01-sddd/` traz `prd.md` + `spec.md` + `dependencies.md`. (Redação antiga que dizia "SDDR não usa
> `xx-sddd`" e punha os arquivos na raiz plana é **legado** — ver
> [`06-anatomia-de-um-sddr.md`](06-anatomia-de-um-sddr.md).)

**Cada `xx-sddd`:** `prd.md` + `spec.md` + `dependencies.md`.

---

## Estrutura obrigatória e ciclo de vida

Todo plano vive em `plans/`, na subpasta do seu status: `01-draft/`, `02-ready/`, `03-running/`,
`blocked/`, `04-completed/` ou `abandoned/` (o caminho feliz é numerado para ordenar; `blocked` e
`abandoned` ficam sem número). **A subpasta corresponde ao `Status:` do `status.md`** — o `Status:`
guarda só o nome do estado (ex.: `running`), e a subpasta é `03-running`; mudou o status, move-se a
pasta. Só o plano de topo (AP ou SDDR) é posicionado por status; subplanos `__sp` ficam aninhados no
AP.

- **`plans/abandoned/`** é histórico **imutável**; não se retoma no mesmo diretório; retomar exige
  um novo plano em `plans/01-draft/`.
- **AP:** não existe `backup-plans/`; todo subplano nasce com `01-sddd/`; `reports/` ficam na raiz
  do subplano, não dentro do `xx-sddd`.

---

## Status

Todo plano e subplano tem `status.md`. Estados oficiais:
`draft` · `ready` · `running` · `blocked` · `completed` · `abandoned`.

Cada estado é também uma subpasta de `plans/`, e o `status.md` do plano de topo determina onde ele
vive. Sem `status.md` não existe execução válida. No subplano AP, o estado oficial é sempre o
`status.md` da **raiz do `__sp`**.

---

## Dependências

Explícitas, sempre. `dependencies.md` é obrigatório em cada `xx-sddd` e em SDDR quando houver
dependência. **Dependência implícita é erro de método.**

---

## Reports

Todo plano executado gera relatórios — a base de prova de execução, transferência de contexto e
histórico técnico. No subplano AP, o `reports/` da raiz documenta o que foi executado nos `xx-sddd`
e registra os *handoffs*. **Arquivo existente mas incompleto não satisfaz o método.**

---

## Auditoria de agente

Gavetas: global (`references/agent-audit/`) e por plano
(`<plano>/references/agent-audit/`). Mínimo por run: `run.md` (+ `artifacts/` opcional).
**Handoff não fica em `agent-audit/`** — fica em `reports/` ou na resposta final do agente.

---

## Promoção para `references/`

Só promova quando a informação for repo-wide, realmente global e melhor consumida fora do plano
original (ex.: identidade atual do sistema, contratos globais, índice histórico residual).

---

## Definition of Done (DoD)

Um plano só é concluído quando:

1. todos os contratos foram cumpridos;
2. dependências foram resolvidas;
3. relatórios obrigatórios existem e estão completos;
4. `status.md` indica `completed`.

Só após isso o plano vai para `plans/04-completed/`. (AP também exige o pacote de
`final-reports/` completo.)

---

## Antipadrões (não faça)

```text
✗ tratar plano histórico como contexto vivo sem promoção específica
✗ usar references/ para duplicar o que já está melhor explicado em subplano ou sddd
✗ criar backup-plans/ em AP
✗ colocar reports dentro de xx-sddd
✗ abrir 02-sddd/ antes de 01-sddd/ existir
✗ assumir dependência implícita
✗ gravar handoff em agent-audit/
✗ manter o status.md numa subpasta de plans/ diferente do seu próprio Status:
✗ começar a descoberta de contexto por leitura bruta de tudo
```
