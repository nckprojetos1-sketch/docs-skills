# inits

Guias oficiais de entrada de agentes no metodo DOCS.

## Regra estrutural

Existe somente uma raiz oficial de inits:

- `init-agents/`

O metodo nao usa mais:

- `init-plans/`
- `init-bootstrap-agent.md` como init autonomo

## Inits oficiais

- `init-agents/init-plan-ap-agent.md`
  - abrir AP e guiar conversa de planejamento
- `init-agents/init-plan-sddr-agent.md`
  - abrir SDDR e guiar conversa de planejamento
- `init-agents/init-executor-agent.md`
  - entrada principal para executar mudanca tecnica ou documental
- `init-agents/init-reviewer-agent.md`
  - revisar metodo, references e historico

## Regra de entrada

Para alterar o sistema, o agente deve entrar primeiro por:

- `init-agents/init-executor-agent.md`

Os outros inits existem para papeis especificos:

- planner AP: abrir estrutura de AP;
- planner SDDR: abrir estrutura de SDDR;
- reviewer: revisar coerencia documental e indexacao.

## Regras comuns

Todo init deve respeitar:

1. verdade do sistema:
   - codigo vivo
   - plano, subplano ou sddd relevante
   - `references/` como indice
   - historico restante
2. fluxo de descoberta:
   - `help/bootstrap-core.md`
   - `references/_generated/context-registry-bootstrap.json`
   - `best_entry_path`
   - `references/_generated/context-registry.json` apenas quando faltarem sinais
   - `references/_generated/context-registry-for-humans/<bucket>.md` apenas quando a busca ainda estiver ampla
   - codigo correlato

## Regra de auditoria

Toda sessao relevante pode usar uma gaveta de auditoria:

- global: `references/_generated/agent-audit/`
- por plano: `<plano>/references/agent-audit/`

Formato minimo:

- `run.md`
