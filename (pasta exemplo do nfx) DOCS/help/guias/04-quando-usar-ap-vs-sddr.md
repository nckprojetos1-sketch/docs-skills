# 04 — Quando usar AP, SDDR ou AN

A primeira decisão de qualquer trabalho é: **que tipo de plano abrir?** Errar aqui gera ou
burocracia demais (AP para um ajuste trivial) ou estrutura de menos (SDDR para algo que precisava
ser coordenado em várias frentes).

---

## A regra de bolso

```text
             A mudança é estrutural, grande ou toca várias frentes/módulos?
                          │                              │
                         SIM                            NÃO
                          │                              │
                          ▼                              ▼
                   Abrir um  AP                   A mudança é local,
              (decompõe em subplanos)          pequena e bem delimitada?
                                                       │
                                                      SIM
                                                       │
                                                       ▼
                                                 Abrir um SDDR

     Ainda não sei quem é o "dono" do contexto  →  use $docs-analyze para decidir
     Preciso primeiro diagnosticar um repo existente  →  trilha AN (em construção)
```

---

## Tabela de decisão

| Critério | AP (`__ap`) | SDDR (`__sddr`) | AN (`__an`) |
| --- | --- | --- | --- |
| **Tamanho** | Grande | Pequeno / local | — (diagnóstico) |
| **Impacto arquitetural** | Alto | Baixo | Investiga |
| **Decompõe em subplanos?** | Sim (`__sp`) | Não | Não |
| **Coordena múltiplos módulos/frentes?** | Sim | Não | — |
| **Estrutura interna** | `architecting-plan/` + subplanos + `final-reports/` | `01-sddd/` na raiz | *Coming Soon* |
| **Quando escolher** | rebuild, nova plataforma, refatoração ampla | corrigir um bug, um endpoint, um ajuste isolado | mapear/entender um repo antes de decidir |

---

## Exemplos concretos

**Casos de AP:**

- "Reconstruir o backend fiscal do zero, com API, workers, ingestão e exportação." → é o
  `nfx-rebuild__ap` deste repositório, com 16 subplanos.
- "Introduzir multi-tenancy em todo o sistema."
- "Migrar de um monólito para serviços separados."

**Casos de SDDR:**

- "Migrar o schema legado para o novo formato." → é o
  `legacy-to-rebuild-schema-migration__sddr` deste repositório.
- "Adicionar um campo `cnpj` na tela de cadastro e validá-lo."
- "Corrigir o cálculo de imposto em uma função específica."

**Casos de AN (quando existir):**

- "Não conheço este repositório; preciso de um inventário técnico e um mapa de riscos antes de
  planejar qualquer mudança."

---

## Na dúvida, use `$docs-analyze`

Se não estiver claro **qual plano já é dono** do contexto (ou se é preciso criar um novo), a skill
`$docs-analyze` faz o diagnóstico: ela encontra o **dono mais estreito** do contexto e devolve uma
recomendação — exatamente uma de:

- `use-existing-plan` (já existe um dono; atualize-o),
- `create-sddr` (abra um SDDR),
- `create-ap` (abra um AP).

Ela também aponta **quais** `prd.md`/`spec.md`/`reports/`/`status.md`/`dependencies.md` um executor
deverá atualizar depois. Ver [`07-as-skills-docs.md`](07-as-skills-docs.md).

---

## Preferência pelo dono mais estreito

Quando um plano já existe, prefira o responsável **mais específico**:

```text
raiz de SDDR   <   raiz de subplano AP   <   raiz de AP
(mais estreito)                              (mais amplo)
```

Só suba de nível quando o escopo realmente exigir.
