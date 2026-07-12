# 08 — O fluxo de ponta a ponta

Este guia mostra como as peças e as skills se encadeiam, da ideia até a entrega e revisão.

---

## O mapa completo

```text
        (opcional) requisito em PDF
                    │
                    ▼
        ┌───────────────────────┐
        │   $docs-pdf-context    │  extrai o PDF para references/<slug>/
        └───────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │      $docs-init        │  valida/cria a raiz DOCS e ROTEIA o pedido
        └───────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │     $docs-analyze      │  quem é o dono? recomenda: usar / SDDR / AP
        └───────────────────────┘
              │              │
        create-ap        create-sddr
              │              │
              ▼              ▼
   ┌──────────────┐   ┌──────────────┐
   │ $docs-plan-ap│   │$docs-plan-sddr│  PLANEJAM (não executam código)
   └──────────────┘   └──────────────┘
              │              │
              └──────┬───────┘
                     ▼
        ┌───────────────────────┐
        │     $docs-executor     │  EXECUTA; atualiza status.md e reports/
        └───────────────────────┘
                     │
                     ▼
        ┌───────────────────────┐
        │  Definition of Done?   │  contratos + deps + reports + status=completed
        └───────────────────────┘
                     │ sim
                     ▼
        plano ──►  plans/04-completed/     (AP também exige final-reports/ completo)
                     │
                     ▼
        ┌───────────────────────┐
        │$docs-clean-plan-context│  consolida contexto; apaga prd/spec obsoletos
        └───────────────────────┘
                     │
                     ▼
        ┌───────────────────────┐
        │     $docs-reviewer     │  audita coerência, índices e movimentações
        └───────────────────────┘
```

---

## Passo a passo narrado

1. **(Opcional) Preparar requisitos.** Se o requisito veio em PDF, rode `$docs-pdf-context` para
   extraí-lo em `references/<slug>/`. Isso vira um *handoff* autossuficiente para o
   planejamento.
2. **Entrar / dar bootstrap.** Rode `$docs-init`. Ele valida (ou cria) a raiz DOCS e **encaminha**
   seu pedido para a skill certa. Toda outra skill "quica" aqui se a raiz estiver ausente.
3. **Diagnosticar o dono.** Quando não estiver claro onde a mudança pertence, rode `$docs-analyze`.
   Ele devolve o dono mais estreito ou uma recomendação (`use-existing-plan` / `create-sddr` /
   `create-ap`) e diz exatamente quais arquivos atualizar.
4. **Planejar.** Abra o plano em `plans/01-draft/`: `$docs-plan-ap` (estrutural) ou `$docs-plan-sddr` (local).
   Os planners escrevem o PRD/SPEC inicial e param em "pronto para executar" — **sem código**.
5. **Executar.** Rode `$docs-executor` contra o plano/subplano/SDDD. Ele trata o código vivo como
   verdade máxima, roda as validações e atualiza `status.md` (quando o estado real muda) e `reports/`
   (prova de execução + handoff).
6. **Concluir e mover para `completed`.** Quando a DoD é atingida (contratos cumpridos, dependências
   resolvidas, reports completos, `status.md = completed`; para AP, também o pacote de
   `final-reports/`), a pasta do plano é movida para `plans/04-completed/`.
7. **Consolidar/limpar contexto.** Rode `$docs-clean-plan-context`. Ele escreve o
   `report-context-consolidation.md` com o contexto durável e apaga os `prd.md`/`spec.md` já
   obsoletos — para que agentes futuros leiam os **reports**, não contratos vencidos.
8. **Revisar a coerência.** Rode `$docs-reviewer` para auditar índices, curadoria de `references/`,
   histórico, consistência dos planos ativos e as movimentações entre as subpastas de status de
   `plans/`. Cada item sai com uma decisão registrada.

---

## Regras que valem o fluxo inteiro

- Obedeça sempre à **hierarquia da verdade** (código > plano > references > histórico).
- Descubra contexto **barato**: índice → melhor ponto de entrada → código. Nunca leia tudo de cara.
- Registre memória curta por run em `agent-audit/` (`YYYY-MM-DD__papel__slug/run.md`).
- **Handoff nunca fica em `agent-audit/`** — fica em `reports/` ou na resposta final do agente.

---

## Próximos passos

- Consulte a regra estrutural completa em [`09-convencoes.md`](09-convencoes.md).
- Veja tudo isso aplicado a um caso real em [`10-exemplo-passo-a-passo.md`](10-exemplo-passo-a-passo.md).
