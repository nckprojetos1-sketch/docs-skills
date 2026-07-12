# 10 — Exemplo passo a passo (caso real)

Nada ensina melhor que um caso concreto. Vamos percorrer um subplano **real** deste repositório,
como um executor faria, do zero até a entrega.

Cenário: executar o subplano
`plans/03-running/nfx-rebuild__ap/01-base-tecnica-runtime-plataforma__sp`.

---

## Passo 0 — Entender onde estou

O trabalho pertence a um **AP** (`nfx-rebuild__ap`), na fatia **subplano 01**. Como já existe um
plano dono, não preciso criar nada — vou **executar**. (Se eu não soubesse disso, rodaria
`$docs-analyze` primeiro para confirmar o dono.)

---

## Passo 1 — Descobrir contexto barato

Sigo o fluxo de descoberta, sem ler o repositório inteiro:

```text
references/README.md
  → o plano dono do tema "base técnica / runtime" (nfx-rebuild__ap)
    → o subplano 01
      → o código correlato (go.mod, docker-compose.yml, ...)
```

---

## Passo 2 — Ler o contrato do subplano (na ordem certa)

O `execution-prompt.md` do subplano (em `references/`) já lista a leitura obrigatória. Em resumo:

1. `architecting-plan/01-vision.md`, `02-scope-and-modules.md`, `03-dependencies.md` (o topo do AP);
2. `01-base-tecnica-runtime-plataforma__sp/status.md` (o estado oficial);
3. `01-sddd/prd.md` (o quê), `01-sddd/spec.md` (como), `01-sddd/dependencies.md` (do que depende);
4. arquivos do repo citados: `README.md`, `go.mod`, `docker-compose.yml`, `.env.example`, `Makefile`.

> Repare: o `execution-prompt.md` também traz **decisões travadas** (ex.: "use Postgres como fonte
> canônica", "não use Redis como fila") e **bloqueios de arquitetura** — coisas que o executor não
> pode violar sem parar e registrar o conflito.

---

## Passo 3 — Executar (com `$docs-executor`)

Trato o **código vivo como verdade máxima** e o subplano como o **contrato**. Executo o que o
`prd.md`/`spec.md` pedem, rodando as validações que o `spec.md` define (ex.:
`go test ./...`, `docker compose config`). Se a realidade do repo divergir do "estado inicial
esperado", **adapto preservando a intenção** e registro a diferença.

---

## Passo 4 — Registrar a prova em `reports/`

Ao terminar, crio um report em
`01-base-tecnica-runtime-plataforma__sp/reports/2026-06-18__execution-report.md` contendo, no mínimo:

- resumo do que foi implementado;
- arquivos criados/alterados e comandos adicionados;
- variáveis de ambiente e portas;
- testes executados + saída resumida;
- falhas, bloqueios e pendências para o próximo subplano.

Esse report **é** o handoff — não deixo isso em `agent-audit/`.

---

## Passo 5 — Atualizar o `status.md`

Atualizo o `status.md` da raiz do subplano para refletir o estado real: por exemplo, de `ready`
para `running` e, ao fechar o ciclo com a DoD atingida, para `completed`. Ligo o resultado ao report
criado.

---

## Passo 6 — Deixar rastro curto em `agent-audit/`

Registro a run em
`nfx-rebuild__ap/references/agent-audit/2026-06-18__executor__base-tecnica-runtime/run.md` — memória
operacional curta (o que fiz, decisões, próximos passos). O handoff detalhado continua em `reports/`.

---

## Passo 7 (mais tarde) — Fechar o AP

Quando **todos** os subplanos estiverem `completed` e o pacote de `final-reports/` estiver completo
(mestre + anexos + checklist), o AP inteiro é movido para `plans/04-completed/`. Depois,
`$docs-clean-plan-context` consolida o contexto durável e remove os
`prd.md`/`spec.md` já vencidos, e `$docs-reviewer` audita a coerência final.

---

## O que este exemplo ensina

| Lição | Onde apareceu |
| --- | --- |
| Contexto se descobre barato, do índice ao código | Passo 1 |
| O plano é o contrato; o código é a verdade | Passos 2–3 |
| Toda execução deixa prova em `reports/` | Passo 4 |
| O estado vive no `status.md` | Passo 5 |
| Memória curta ≠ handoff | Passo 6 |
| Concluir tem gate (DoD + final-reports) | Passo 7 |

Pronto para começar? Copie um esqueleto em [`../templates/`](../templates/) e mãos à obra.
