# init-agents

`init-agents/` agrupa os unicos inits oficiais do metodo.

Eles existem para que cada tipo de agente saiba:

- como iniciar a conversa;
- quais arquivos ler primeiro;
- qual e a saida esperada;
- quando atualizar o indice do DOCS.

## Arquivos

- `init-plan-ap-agent.md`
  - planner para abrir AP
- `init-plan-sddr-agent.md`
  - planner para abrir SDDR
- `init-executor-agent.md`
  - porta principal para alterar o sistema
- `init-reviewer-agent.md`
  - reviewer de metodo

## Regras comuns

1. verdade do sistema:
   - codigo vivo
   - plano, subplano ou sddd relevante
   - `references/` como indice
   - historico restante
2. fluxo base:
   - `help/bootstrap-core.md`
   - `references/README.md`
   - `references/_generated/context-registry-bootstrap.json`
   - `best_entry_path`
   - `references/_generated/context-registry.json` apenas quando faltarem sinais
   - `references/_generated/context-registry-for-humans/<bucket>.md` apenas quando a busca ainda estiver ampla
   - codigo correlato
3. toda execucao relevante pode registrar memoria operacional em:
   - global: `DOCS-Engenharia-de-Contexto/references/_generated/agent-audit/`
   - por plano: `<plano>/references/agent-audit/`

## Regra de prioridade

Quando a intencao for alterar o sistema, o init correto e:

- `init-executor-agent.md`

Os planners abrem estrutura e escrevem documentacao inicial.

O reviewer verifica coerencia do metodo e da indexacao.

## Formato minimo de run

Cada run deve usar uma pasta:

- `YYYY-MM-DD__agent-role__slug/`

Arquivos minimos:

- `run.md`
- `artifacts/` opcional
