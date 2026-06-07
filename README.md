# DOCS Skills

Pacote de skills DOCS para agentes Codex.

Este repositorio distribui skills operacionais que ajudam agentes a iniciar,
planejar, executar e revisar trabalho com contexto estruturado. O metodo DOCS
continua documentado em `help/`; este README foca em como instalar e usar as
skills deste pacote.

## Quick Start

De qualquer ambiente com Node/npm instalado, instale direto do GitHub com:

```powershell
npx --yes github:nckprojetos1-sketch/docs-skills
```

Para atualizar as skills instaladas com a versao mais recente deste repositorio:

```powershell
npx --yes github:nckprojetos1-sketch/docs-skills update
```

Para limpar skills DOCS antigas que nao fazem parte deste pacote e instalar as
novas:

```powershell
npx --yes github:nckprojetos1-sketch/docs-skills --clean-docs
```

Se voce ja clonou este repositorio, tambem pode instalar ou atualizar com:

```powershell
cd C:\Repositorios\docs-skills
python .\scripts\install_docs_skills.py
```

Depois da instalacao, reinicie o Codex para carregar as skills novas.

## Skills Incluidas

### `$docs-init`

Use quando um repositorio ainda nao tem `DOCS-Engenharia-de-Contexto/` ou quando
voce quer validar se a estrutura DOCS basica existe.

O que ela faz:

- detecta o repositorio alvo a partir do diretorio atual ou do caminho informado;
- cria ou valida a raiz `DOCS-Engenharia-de-Contexto/`;
- confere entradas minimas como `README.md`, `help/`, `references/`,
  `plans-to-be-executed/`, `plans-executed/` e `plans-abandoned/`;
- reporta o que foi criado, normalizado, validado, avisos e erros.

Importante: `docs-init` e de uso unico. Depois de uma inicializacao ou validacao
bem-sucedida, ela orienta o agente a pedir permissao para remover a propria skill
de `~/.codex/skills/docs-init` e `~/.agents/skills/docs-init`. As outras skills
DOCS nao sao removidas.

### `$docs-plan-ap`

Use quando a mudanca precisa de planejamento arquitetural antes da execucao.
E a skill certa para trabalhos com varios modulos, dependencias entre frentes,
subplanos ou risco de decisao arquitetural mal documentada.

O que ela faz:

- conduz uma conversa de planejamento, sem alterar codigo;
- fecha objetivo, motivacao, escopo, fora de escopo, areas impactadas, riscos,
  dependencias e criterios de aceite;
- cria um Architecting Plan em `plans-to-be-executed/`;
- estrutura o AP com `architecting-plan/`, `final-reports/`, `status.md`,
  auditoria e subplanos `NN-*__sp`;
- cria em cada subplano a base `01-sddd/` com `prd.md`, `spec.md` e
  `dependencies.md`.

Entrega esperada: um AP pronto para handoff, com subplanos claros e contexto
suficiente para um executor implementar sem reconstruir a decisao do zero.

### `$docs-plan-sddr`

Use quando a mudanca e pequena, local ou bem delimitada, mas ainda precisa de
PRD/SPEC antes de alguem executar. E a alternativa mais leve ao AP.

O que ela faz:

- conduz uma conversa curta de planejamento, sem executar codigo;
- define objetivo, problema, limites de escopo, riscos, restricoes, criterios de
  aceite e comandos de validacao esperados;
- cria um SDDR em `plans-to-be-executed/`;
- gera `status.md`, `reports/`, auditoria do plano e `01-sddd/`;
- cria em cada `xx-sddd/` `prd.md`, `spec.md` e `dependencies.md`.

Entrega esperada: um plano compacto, objetivo e executavel para uma mudanca
local. Ela usa `xx-sddd/` direto na raiz do SDDR, sem subplano `__sp`.

### `$docs-pdf-context`

Use quando voce tem um PDF de requisitos e quer preparar contexto enxuto antes
de abrir um AP ou SDDR. Ela nao cria plano; apenas transforma o PDF em material
consultavel.

O que ela faz:

- valida o PDF informado e detecta se ha DOCS instalado no repositorio;
- extrai texto por pagina, secoes, requisitos, endpoints e criterios de aceite;
- extrai tabelas com PyMuPDF quando possivel e usa `pypdf` como fallback de
  texto;
- gera `README.md` em `DOCS-Engenharia-de-Contexto/references/global/<pdf>/`
  quando DOCS existe, ou em `<pdf-slug>/` ao lado do PDF quando nao
  existe;
- gera `context.json` como extracao intermediaria para revisao do agente;
- aceita `--out <diretorio>` para usar exatamente uma saida manual;
- cria `tables.json` somente quando houver tabelas reais detectadas, com
  `table_id` e `row_id` citados no README;
- falha com mensagem clara para PDFs escaneados ou sem texto extraivel, sem
  inventar contexto.

Entrega esperada: um pacote de contexto com sintese operacional, requisitos,
fluxos explicitos ou inferidos, criterios de aceite, restricoes e
rastreabilidade por pagina, pronto para ser usado por `$docs-plan-ap` ou
`$docs-plan-sddr`.

### `$docs-executor`

Use quando ja existe um plano, subplano, SDDDR ou SDDR e voce quer que o agente
execute a mudanca com base nesse contrato.

O que ela faz:

- confirma que o repositorio tem DOCS instalado;
- le o bootstrap minimo, o indice de referencias e o plano relevante;
- identifica o trabalho ativo e a area de codigo/documentacao a inspecionar;
- antes de alterar arquivos, fecha alvo, mudanca esperada, validacoes e quais
  artefatos DOCS precisam ser atualizados;
- executa a mudanca respeitando a hierarquia: codigo vivo primeiro, plano
  relevante depois, `references/` como apoio e indice;
- atualiza `status.md`, `reports/`, registros de auditoria ou indices apenas
  quando isso fizer sentido para a execucao.

Entrega esperada: a mudanca implementada, validada quando possivel, com resumo
claro do que foi feito e dos artefatos DOCS atualizados.

### `$docs-reviewer`

Use para revisar a coerencia do metodo DOCS dentro de um repositorio. Ela nao e
uma skill de code review de produto; o foco e qualidade estrutural do contexto.

O que ela revisa:

- qualidade e consistencia dos indices em `references/_generated/`;
- se `references/global/` contem apenas informacao realmente global;
- planos ativos, executados ou abandonados;
- movimentacoes entre `plans-to-be-executed/`, `plans-executed/` e
  `plans-abandoned/`;
- aderencia a convencoes, governanca, Definition of Done e estrutura esperada;
- necessidade de promover contexto para global, manter em plano, abandonar plano
  ou corrigir indice.

Entrega esperada: achados primeiro, agrupados por severidade ou risco de metodo,
com evidencia consultada, justificativa, risco e proximo passo recomendado.

### `$docs-clean-plan-context`

Use depois que um SDDR ou subplano de AP ja foi implementado e marcado como
`completed`, quando `prd.md` e `spec.md` deixaram de ser a melhor fonte de
contexto e os reports devem assumir esse papel.

O que ela faz:

- confirma que o alvo esta `completed` e possui reports de execucao;
- le `prd.md`, `spec.md` e os reports existentes;
- cria ou atualiza `reports/report-context-consolidation.md`;
- move para esse report o problema original, objetivo, solucao semantica,
  escopo util, criterios de aceite e areas impactadas;
- apaga apenas `prd.md` e `spec.md` depois da consolidacao;
- preserva `dependencies.md`, `status.md`, reports existentes e auditoria;
- atualiza indices somente se PRD/SPEC eram pontos de entrada indexados.

Entrega esperada: um plano concluido mais enxuto, onde reports explicam tanto o
que foi implementado quanto o contexto semantico necessario para entender por
que a implementacao existe.

## Como o Instalador Funciona

O script `scripts/install_docs_skills.py`:

- copia as skills de `skills/` para `~\.codex\skills`;
- instala tambem `docs-init` em `~\.agents\skills`;
- valida `SKILL.md` e `agents/openai.yaml` de cada skill;
- cria backup das versoes anteriores em `~\.codex\skills-backups`;
- desativa skills legadas `xml-docs-init-*` apos copiar e validar as novas.

Para manter as skills legadas ativas durante a instalacao:

```powershell
npx --yes github:nckprojetos1-sketch/docs-skills --keep-legacy
```

Para ver as opcoes do instalador:

```powershell
npx --yes github:nckprojetos1-sketch/docs-skills --help
```

O comando `update` e um alias explicito de instalacao: ele baixa o pacote atual
do GitHub e substitui as skills instaladas por esta versao, preservando backup.

## Estrutura do Repositorio

```text
docs-skills/
|-- README.md
|-- package.json
|-- bin/
|   `-- install-docs-skills.js
|-- scripts/
|   `-- install_docs_skills.py
|-- skills/
|   |-- docs-init/
|   |-- docs-executor/
|   |-- docs-pdf-context/
|   |-- docs-plan-ap/
|   |-- docs-plan-sddr/
|   |-- docs-reviewer/
|   `-- docs-clean-plan-context/
`-- help/
    |-- bootstrap-core.md
    |-- conventions.md
    |-- inits/
    `-- templates/
```

## Desenvolvimento Das Skills

Cada skill vive em `skills/<nome-da-skill>/` e deve conter:

- `SKILL.md` com frontmatter valido;
- `agents/openai.yaml` com a politica de invocacao;
- `references/` quando a skill precisar de contexto de apoio;
- `scripts/` quando houver automacao propria da skill.

Depois de alterar qualquer skill, rode novamente:

```powershell
npx --yes github:nckprojetos1-sketch/docs-skills --clean-docs
```

O instalador valida as fontes antes de substituir as skills instaladas.

## Documentacao De Apoio

- `help/bootstrap-core.md` resume o nucleo do metodo usado pelas skills.
- `help/conventions.md` define convencoes estruturais.
- `help/inits/` guarda prompts e entradas historicas de agentes.
- `help/templates/` guarda modelos usados por AP e SDDR.
