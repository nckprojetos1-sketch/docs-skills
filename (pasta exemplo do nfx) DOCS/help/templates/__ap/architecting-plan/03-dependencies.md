# architecting-plan · 03 — Dependências

## Dependências entre subplanos
Quais subplanos dependem de quais. Torne toda dependência **explícita** — dependência implícita é
erro de método.

| Subplano | Depende de | Motivo |
| --- | --- | --- |
| `02-...__sp` | `01-...__sp` | precisa da base técnica pronta |

## Dependências externas
- serviços, credenciais, integrações de terceiros;
- decisões de produto pendentes.

## Ordem de execução sugerida
```text
01 → 02 → (03, 04 em paralelo) → 05 ...
```

## Bloqueios conhecidos
- liste impedimentos atuais e o que os destrava.
