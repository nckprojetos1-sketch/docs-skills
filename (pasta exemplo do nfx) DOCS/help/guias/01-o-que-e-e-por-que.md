# 01 — O que é o DOCS e por que ele existe

## Resumo

DOCS (**Engenharia de Contexto**) é um método para organizar o trabalho de software feito com
apoio de IA. A ideia central, repetida em toda a documentação do método:

> **Documentação, aqui, não é subproduto. É infraestrutura operacional.**

Ou seja: os documentos não existem para "registrar depois". Eles são a estrutura que torna possível
planejar, executar, revisar e passar o bastão (*handoff*) de forma previsível.

---

## O problema que o DOCS resolve

Trabalho assistido por IA (e trabalho em equipe em geral) sofre de quatro males:

1. **Memória volátil.** O agente/pessoa esquece o contexto entre sessões.
2. **Janela de contexto limitada.** Não dá para ler o repositório inteiro toda vez.
3. **Decisões sem rastro.** Ninguém sabe por que algo foi feito daquele jeito.
4. **Handoff imprevisível.** Passar a tarefa adiante vira arqueologia.

O DOCS ataca os quatro:

- **externaliza a memória operacional** — o contexto vive em arquivos, não na cabeça de ninguém;
- **dá rastreabilidade** às decisões e à execução;
- **separa** contexto vivo, índice e histórico bruto;
- torna **execução, revisão e continuidade previsíveis**.

---

## A hierarquia da verdade

Esta é a espinha dorsal do método. Quando duas fontes divergem, vale a que estiver mais acima:

```text
   ┌─────────────────────────────────────────────┐
   │  1. CÓDIGO VIVO do repositório                │  ← verdade máxima
   ├─────────────────────────────────────────────┤
   │  2. PLANO / SUBPLANO / SDDD relevante         │  ← o contrato de execução
   ├─────────────────────────────────────────────┤
   │  3. references/  (índice e apoio global)      │  ← aponta, não substitui
   ├─────────────────────────────────────────────┤
   │  4. HISTÓRICO restante                        │  ← só quando promovido
   └─────────────────────────────────────────────┘
```

Regras que decorrem disso:

- `references/` **aponta** para o contexto, mas **nunca substitui** plano nem código;
- um plano histórico **não vira contexto vivo automaticamente** — precisa de promoção explícita;
- o contexto vivo deve continuar no **melhor ponto de manutenção** (normalmente o plano ou o código),
  e não ser recontado em vários lugares;
- o `help/` (este material) define o **método**, não o estado real de execução.

---

## Os princípios operacionais

| Princípio | O que significa na prática |
| --- | --- |
| **Bootstrap barato** | Começa-se pelo índice curto e dirigido, não lendo tudo. |
| **Não duplicar contexto** | Se algo já está bem explicado num plano, não se recopia para `references/`. |
| **Estado sempre explícito** | Todo plano/subplano tem um `status.md`. Sem ele, não há execução válida. |
| **Rastreabilidade** | Toda execução gera `reports/`; toda run deixa registro curto em `agent-audit/`. |
| **Um lar por plano** | Cada plano está em exatamente uma das pastas de ciclo de vida. |

---

## O que o DOCS **não** é

- Não é um substituto do código — código vivo é a verdade máxima.
- Não é um repositório de "documentação de marketing" ou wiki genérica.
- Não é lugar para duplicar contexto que já vive melhor num plano ou no próprio código.
- O `agent-audit/` não é lugar de *handoff* — *handoff* vive em `reports/` ou na resposta final
  do agente.

---

## Próximos passos

- Aprenda o vocabulário em [`02-conceitos-e-glossario.md`](02-conceitos-e-glossario.md).
- Veja como as pastas materializam esses princípios em
  [`03-estrutura-de-pastas.md`](03-estrutura-de-pastas.md).
