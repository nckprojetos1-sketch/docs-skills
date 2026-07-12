# 06 — Anatomia de um SDDR

Um SDDR (**Spec-Driven Development with Reports**) é o plano leve, para uma mudança local, pequena
e bem delimitada. Ele não se decompõe em subplanos.

---

## Estrutura canônica

```text
<nome>__sddr/
├── status.md                  # estado oficial do SDDR
├── 01-sddd/                   # a etapa de planejamento+execução
│   ├── prd.md
│   ├── spec.md
│   └── dependencies.md
├── references/
│   └── agent-audit/           # gaveta de runs deste SDDR
└── reports/                   # prova de execução e handoffs
```

O `dependencies.md` é obrigatório sempre que houver uma dependência explícita.

---

## ⚠️ Reconciliação: qual estrutura é a certa?

Existe uma **incoerência histórica** na documentação do método. Você pode encontrar duas versões:

| Versão | O que diz | Situação |
| --- | --- | --- |
| **Prosa antiga** (método canônico original) | "SDDR **não** usa `xx-sddd`"; os arquivos (`prd.md`, `spec.md`...) ficam soltos na **raiz** do plano. | **Legado.** |
| **Ferramentas + skills + prática atual** | O SDDR usa uma pasta **`01-sddd/`** com `prd.md`/`spec.md`/`dependencies.md`. | **Canônico (siga esta).** |

Este material adota a **segunda** versão como canônica, porque é o que o gerador (`create_sddr.py`),
as skills (`$docs-plan-sddr`, `$docs-analyze`, `$docs-clean-plan-context`) e os planos reais
efetivamente produzem. Trate a prosa antiga apenas como redação a ser reconciliada.

---

## Exemplo real: `legacy-to-rebuild-schema-migration__sddr`

Este repositório tem um SDDR ativo em
`plans/blocked/legacy-to-rebuild-schema-migration__sddr`. Sua estrutura real:

```text
legacy-to-rebuild-schema-migration__sddr/
├── status.md
├── 01-sddd/
│   ├── prd.md
│   ├── spec.md
│   ├── dependencies.md
│   └── execution-prompt.md                  # prompt de execução desta etapa
├── references/
│   ├── 2026-06-08__execute-...-prompt.md
│   └── agent-audit/
│       └── 2026-06-08__planner-sddr__legacy-to-rebuild-schema-migration/run.md
└── reports/
    ├── 2026-06-08__legacy-inventory-and-gap-analysis.md
    ├── 2026-06-08__legacy-fiscal-dry-run/          (report.md + report.json)
    └── 2026-06-08__nfx-rebuild-schema-apply-and-fiscal-migration/  (migration-report.*)
```

Repare em três coisas didáticas neste exemplo:

1. **Usa `01-sddd/`** — confirmando a versão canônica atual.
2. O **prompt de execução** está em `01-sddd/execution-prompt.md` (em SDDR ele costuma acompanhar a
   etapa; em subplanos de AP deste repo, ele vive em `references/`).
3. Os `reports/` guardam evidências reais e ricas — inclusive subpastas com `report.md` + `report.json`
   por run. É a **prova de execução** do método em ação.

---

## Como um SDDR difere de um AP

| | SDDR | AP |
| --- | --- | --- |
| Subplanos (`__sp`) | não tem | tem um ou mais |
| `architecting-plan/` | não tem | tem |
| `final-reports/` | não tem | tem (obrigatório para migrar) |
| Etapas `xx-sddd` | uma (`01-sddd`), na raiz | uma ou mais, dentro de cada subplano |
| Peso | leve | estrutural |

---

## Próximos passos

- Veja quais skills abrem e executam um SDDR em [`07-as-skills-docs.md`](07-as-skills-docs.md).
- Copie um esqueleto pronto em [`../templates/__sddr/`](../templates/__sddr/).
