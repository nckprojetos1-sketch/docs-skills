# Help do método DOCS — guia didático

Bem-vindo. Este é o material de ajuda **didático** do método **DOCS — Engenharia de Contexto**.
Ele ensina, do zero, o que é o método, para que serve e como usá-lo no dia a dia — para pessoas
e para agentes de IA.

> **De onde vem este material:** foi escrito a partir de três fontes combinadas — as *skills*
> oficiais `$docs-*` (a definição canônica do método), o `README.md` e o `help/` originais do
> repositório, e a forma como os planos **realmente construídos** em `plans/`
> estão organizados hoje. Onde havia incoerência entre a teoria antiga e a prática, seguimos a
> prática atual. Este é agora o material oficial do método, aqui em `help/` (guias + templates).

---

## Em uma frase

> **DOCS transforma documentação em infraestrutura operacional:** um jeito previsível de planejar,
> executar, revisar e entregar mudanças de software com rastreabilidade total — sem estourar a
> janela de contexto de quem (ou o quê) está trabalhando.

---

## Entre por intenção

Vá direto ao ponto conforme o que você precisa fazer:

| Você quer... | Comece por |
| --- | --- |
| Entender o que é o método e por que ele existe | [`guias/01-o-que-e-e-por-que.md`](guias/01-o-que-e-e-por-que.md) |
| Saber o significado dos termos (AP, SDDR, SDDD, `__sp`...) | [`guias/02-conceitos-e-glossario.md`](guias/02-conceitos-e-glossario.md) |
| Entender as pastas e o ciclo de vida de um plano | [`guias/03-estrutura-de-pastas.md`](guias/03-estrutura-de-pastas.md) |
| Decidir entre abrir um AP ou um SDDR | [`guias/04-quando-usar-ap-vs-sddr.md`](guias/04-quando-usar-ap-vs-sddr.md) |
| Ver a anatomia completa de um AP | [`guias/05-anatomia-de-um-ap.md`](guias/05-anatomia-de-um-ap.md) |
| Ver a anatomia completa de um SDDR | [`guias/06-anatomia-de-um-sddr.md`](guias/06-anatomia-de-um-sddr.md) |
| Saber quais *skills* usar e como chamá-las | [`guias/07-as-skills-docs.md`](guias/07-as-skills-docs.md) |
| Ver o fluxo de trabalho de ponta a ponta | [`guias/08-fluxo-de-ponta-a-ponta.md`](guias/08-fluxo-de-ponta-a-ponta.md) |
| Consultar a regra estrutural canônica | [`guias/09-convencoes.md`](guias/09-convencoes.md) |
| Aprender vendo um exemplo real, passo a passo | [`guias/10-exemplo-passo-a-passo.md`](guias/10-exemplo-passo-a-passo.md) |
| Copiar um esqueleto pronto de plano | [`templates/`](templates/) |

---

## Ordem de leitura sugerida

Se você está começando agora, leia nesta ordem:

```text
01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 07 -> 08 -> 09 -> 10
(o quê)  (termos)  (pastas)  (AP x SDDR)  (AP)  (SDDR)  (skills)  (fluxo)  (regras)  (exemplo)
```

Se você já conhece o método e só precisa executar, vá direto para o
[guia de fluxo](guias/08-fluxo-de-ponta-a-ponta.md) e para as
[convenções](guias/09-convencoes.md).

---

## As três ideias que sustentam tudo

1. **A verdade tem uma hierarquia.** Código vivo vale mais que plano; plano vale mais que índice;
   índice vale mais que histórico. Ver [guia 01](guias/01-o-que-e-e-por-que.md).
2. **Todo plano tem um lar e um estado.** Ele vive em `plans/`, na subpasta do seu status —
   nunca em duas — e tem sempre um `status.md`. Ver
   [guia 03](guias/03-estrutura-de-pastas.md).
3. **Contexto se descobre barato.** Nunca se começa lendo tudo; começa-se pelo índice e vai-se
   afunilando. Ver [guia 03](guias/03-estrutura-de-pastas.md).
