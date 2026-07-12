# 03 — Estrutura de pastas e ciclo de vida

## A raiz oficial do DOCS

```text
DOCS-Engenharia-de-Contexto/
├── README.md                 # porta de entrada oficial do método
├── help/                     # o método: guias (guias/) e templates (templates/)
├── references/               # contexto transversal do projeto (verdades globais + docs vivas)
└── plans/                    # todos os planos, organizados por status
    ├── 01-draft/             # sendo planejados
    ├── 02-ready/             # prontos para executar
    ├── 03-running/           # execução em andamento
    ├── blocked/              # bloqueados
    ├── 04-completed/         # concluídos (DoD atingida)
    └── abandoned/            # abandonados (histórico imutável)
```

### As três camadas

1. **`help/`** — o **método**: os guias (`guias/`) e os templates (`templates/`). É a documentação
   do método; não guarda estado real de execução.
2. **`references/`** — o **contexto transversal** do projeto e as poucas verdades verdadeiramente
   globais. Aponta para onde buscar; não substitui plano nem código.
3. **`plans/`** — onde **todos os planos vivem**, organizados por status.

---

## O ciclo de vida de um plano

Todo plano (AP ou SDDR) vive em **uma** subpasta de `plans/`, e essa subpasta corresponde ao campo
`Status:` do seu `status.md`.

**Ordenação:** as quatro etapas do caminho feliz recebem um prefixo numérico para ordenar —
`01-draft`, `02-ready`, `03-running`, `04-completed`. Os dois estados fora do caminho (`blocked`,
`abandoned`) ficam **sem** prefixo. O `Status:` guarda só o nome do estado (ex.: `running`); a
subpasta correspondente é `03-running`.

**Invariante:** o `Status:` do `status.md` e a subpasta nunca divergem. Quando o status muda, a
**pasta do plano é movida** para a subpasta correspondente. Não há mais `plans-to-be-executed/`,
`plans-executed/` nem `plans-abandoned/`: o estado é a **localização**.

```text
   nasce em                        avança conforme o status.md
   plans/01-draft/                    (mover a pasta a cada mudança)

   draft ──► ready ──► running ──► completed
                │          │
                ▼          ▼
             blocked    blocked
                │
                ▼
             abandoned   (histórico IMUTÁVEL)
```

Apenas o **plano de topo** (AP ou SDDR) é posicionado por status. Os **subplanos `__sp`** ficam
aninhados dentro do AP e **não** são movidos para subpastas de status — cada um tem seu próprio
`status.md`, mas quem determina a subpasta é o `status.md` da **raiz do AP**.

### Gatilhos de movimentação

| Movimento | Quando acontece |
| --- | --- |
| **criação → `plans/01-draft/`** | Todo novo AP ou SDDR nasce em `plans/01-draft/`. |
| **mudança de status → mover a pasta** | Sempre que o `status.md` muda de estado, mova a pasta do plano para `plans/<novo-status>/`. A subpasta e o `Status:` nunca podem divergir. |
| **→ `plans/04-completed/`** | Somente quando a **Definition of Done** é atingida: contratos cumpridos, dependências resolvidas, reports obrigatórios completos e `status.md = completed`. Para AP, também exige o pacote completo de `final-reports/`. |
| **→ `plans/abandoned/`** | Abandono. `plans/abandoned/` é **imutável** e não deve ser retomado no mesmo diretório. Retomar exige **um novo plano em `plans/01-draft/`**. |

---

## A pasta `references/` da raiz

Ela **não** substitui subplanos, SDDDs ou SDDRs. Existe para guardar o **contexto transversal do
projeto** — verdades globais e documentação viva que vale para vários planos e deve permanecer
atualizada.

Pastas-padrão:

```text
references/
├── README.md
├── agent-audit/            # gaveta global de runs de agente (cross-plan)
├── api-documentations/     # contratos e documentação de APIs — manter atualizada
├── build-documentation/    # build, deploy, Docker/compose, runtime — manter atualizada
├── database-documentation/ # schema, índices, consultas, tuning — manter atualizada
├── execution-references/   # referências transversais consultadas na execução
└── prompts/                # prompts reutilizáveis (inclui prompts de migração do método)
```

`database-documentation/`, `api-documentations/` e `build-documentation/` são o **contexto vivo** do
projeto: mantenha-os atualizados conforme o sistema evolui. Pastas específicas do projeto (ex.:
`IMPORTANTE/`) são permitidas **além** das padrão.

Regra: só promova algo para `references/` quando for repo-wide e melhor consumido fora do plano de
origem. Não duplique aqui o que já vive melhor em um plano, subplano ou no código.

---

## O fluxo de descoberta barato

Nunca comece lendo tudo. Afunile do índice até o código, parando assim que tiver sinal suficiente:

```text
1. references/README.md e as pastas-domínio relevantes
   (database-documentation/, api-documentations/, build-documentation/)
2. localizar o plano do tema em plans/<status>/
3. abrir o status.md do plano e, se preciso, seu xx-sddd/ e reports/
4. o código correlato
```

---

## Auditoria operacional

Duas gavetas oficiais de `agent-audit/`:

- **global:** `references/agent-audit/`
- **por plano:** `<plano>/references/agent-audit/`

Formato canônico de cada run: `YYYY-MM-DD__papel-do-agente__slug/`, com no mínimo um `run.md`
(e um `artifacts/` opcional). Lembre: **handoff não fica em `agent-audit/`** — fica em `reports/`
ou na resposta final do agente.

---

## Próximos passos

- Veja a estrutura interna de um AP em [`05-anatomia-de-um-ap.md`](05-anatomia-de-um-ap.md).
- Veja a de um SDDR em [`06-anatomia-de-um-sddr.md`](06-anatomia-de-um-sddr.md).
