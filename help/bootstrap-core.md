# bootstrap-core

Leitura central do metodo DOCS.

Este arquivo explica o minimo que um agente precisa saber para operar no
repositorio sem abrir varios documentos redundantes.

## O que o DOCS faz

DOCS e a infraestrutura de contexto do repositorio.

Ele existe para:

- externalizar memoria operacional;
- deixar decisoes e execucao rastreaveis;
- separar contexto vivo de indice e historico;
- tornar handoff, revisao e continuidade previsiveis.

## Verdade do sistema

Hierarquia oficial de verdade:

1. codigo vivo do repositorio;
2. plano, subplano ou etapa relevante;
3. `references/` como indice e apoio global;
4. historico restante.

Regras:

- `references/` aponta para contexto, mas nao substitui plano nem codigo;
- plano historico nao vira contexto vivo automaticamente;
- bootstrap deve ser barato e dirigido;
- busca de contexto nunca deve comecar por leitura bruta de tudo.

## Fluxo oficial de descoberta

Fluxo minimo:

1. abrir `references/README.md`;
2. abrir `references/_generated/context-registry-bootstrap.json`;
3. localizar o tema;
4. abrir `best_entry_path`;
5. abrir `references/_generated/context-registry.json` somente se faltarem sinais;
6. abrir `references/_generated/context-registry-for-humans/<bucket>.md` somente se a busca ainda estiver ampla;
7. abrir codigo correlato.

O bootstrap index deve responder, com custo baixo:

- bucket;
- tipo do pacote;
- melhor ponto de entrada;
- estado e classificacao;
- resumo curto do tema.

## Estruturas canonicas atuais

### `references/`

Estrutura oficial:

- `README.md`
- `global/`
- `history/`
- `_generated/`

Uso:

- `global/` guarda somente verdades repo-wide;
- `history/` guarda valor residual historico indexavel;
- `_generated/` guarda `context-registry-bootstrap.json`, `context-registry.json`,
  `context-registry-for-humans/` e `agent-audit/`.

### AP

Usar AP quando houver impacto estrutural, mais de uma frente ou necessidade de
coordenacao entre modulos.

Raiz canonica:

- `architecting-plan/`
- subplanos `NN-nome__sp/`
- `final-reports/`
- `references/agent-audit/`
- `status.md`

Cada subplano AP deve nascer com:

- `status.md`
- `reports/`
- `01-sddd/`

Cada `xx-sddd/` deve conter:

- `prd.md`
- `spec.md`
- `dependencies.md`

### SDDR

Usar SDDR quando a mudanca for local, pequena ou bem delimitada.

Raiz canonica:

- `prd.md`
- `spec.md`
- `status.md`
- `reports/`
- `references/agent-audit/`

`dependencies.md` entra quando houver dependencia explicita.

## Estados e rastreabilidade

Estados oficiais de `status.md`:

- `draft`
- `ready`
- `running`
- `blocked`
- `completed`

Regras:

- todo plano e subplano precisa de `status.md`;
- `reports/` registra prova de execucao e handoffs;
- `agent-audit/` guarda memoria operacional curta;
- handoff nao fica em `agent-audit/`.

## Quando atualizar o DOCS

Atualizar `status.md` e `reports/` quando a execucao mudar estado real do plano.

Atualizar `references/` somente quando houver:

- mudanca de navegacao do tema;
- valor residual historico que precisa ser preservado;
- nova verdade repo-wide.

Nao promover para `references/` o que continua melhor explicado no plano,
subplano ou codigo.

## Glossario minimo

- AP: plano arquitetural para trabalho estrutural ou multi-frente.
- SDDR: plano simples para mudanca local.
- subplano `__sp`: unidade executavel dentro de um AP.
- `xx-sddd`: etapa local dentro de um subplano AP.
- `reports/`: prova de execucao e handoff.
- `agent-audit/`: memoria operacional curta por run.

## Consulta sob demanda

`help/conventions.md` continua sendo a fonte normativa para:

- regra estrutural;
- governanca;
- DoD;
- formato canonico;
- conflito de metodo.
