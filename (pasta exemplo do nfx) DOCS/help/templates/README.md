# Templates limpos do método DOCS

Esqueletos prontos para copiar ao abrir um novo plano. Já refletem a **prática atual** do
repositório e as convenções descritas nos [guias](../guias/) — sem os arquivos vazios ou
contaminados do `help/` original.

## O que tem aqui

```text
templates/
├── __ap/                          # esqueleto de um Architecting Plan
│   ├── status.md
│   ├── architecting-plan/         # 4 documentos de planejamento arquitetural
│   ├── final-reports/             # pacote de consolidação + checklist do gate de conclusão
│   ├── references/agent-audit/    # gaveta de runs do AP
│   └── 01-exemplo-subplano__sp/   # um subplano de exemplo, completo
│       ├── status.md
│       ├── 01-sddd/               # prd.md + spec.md + dependencies.md
│       ├── references/            # execution-prompt.md (prompt de contexto limpo)
│       └── reports/               # README + report-success + report-merge
└── __sddr/                        # esqueleto de um SDDR
    ├── status.md
    ├── 01-sddd/                   # prd.md + spec.md + dependencies.md
    ├── references/agent-audit/
    └── reports/
```

## Como usar

1. **Prefira as skills.** O jeito canônico de abrir um plano é `$docs-plan-ap` ou `$docs-plan-sddr`
   (elas geram a estrutura por você). Ver [`../guias/07-as-skills-docs.md`](../guias/07-as-skills-docs.md).
2. **Ou copie à mão.** Se for criar manualmente, copie a pasta `__ap/` ou `__sddr/` para
   `plans/01-draft/`, renomeie seguindo os sufixos (`<slug>__ap` / `<slug>__sddr`) e preencha
   os arquivos.
3. Renomeie o subplano de exemplo (`01-exemplo-subplano__sp`) para o nome real
   (`NN-<slug>__sp`) e duplique-o para quantos subplanos precisar.

## Lembretes

- Nomes de pasta: minúsculos, `kebab-case`, sem acento (ver [convenções](../guias/09-convencoes.md)).
- Todo plano/subplano precisa de `status.md`.
- O prompt de execução do subplano vive em `references/execution-prompt.md`.
- `final-reports/report-final.md` é obrigatório para mover o AP para `plans/04-completed/`.
