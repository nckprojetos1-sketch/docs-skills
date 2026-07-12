# references

Contexto **transversal** do projeto: verdades e documentação inerentes ao repositório
como um todo, importantes para vários planos. `references/` aponta e centraliza esse
contexto global — **não** substitui plano, subplano nem código.

## Pastas-padrão

Toda raiz DOCS mantém, por padrão, estas pastas:

- `agent-audit/` — gaveta **global** de runs de agente (cross-plan).
- `api-documentations/` — contratos e documentação de APIs. **Manter atualizada.**
- `build-documentation/` — build, deploy, Docker/compose, jobs, workers e runtime. **Manter atualizada.**
- `database-documentation/` — schema, índices, consultas e tuning. **Manter atualizada.**
- `execution-references/` — referências transversais consultadas na execução de vários planos.
- `prompts/` — prompts reutilizáveis (inclui os prompts de migração do método).

`database-documentation/`, `api-documentations/` e `build-documentation/` são o contexto
vivo do projeto que deve permanecer sempre atualizado conforme o sistema evolui.

## Regras

- Pastas específicas de um projeto (ex.: `IMPORTANTE/`) são permitidas **além** das padrão.
- Só promova algo para `references/` quando for repo-wide e melhor consumido fora do plano
  de origem. Não duplique aqui o que já vive melhor em um plano, subplano ou no código.
