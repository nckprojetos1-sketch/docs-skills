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

- `$docs-init`
  - Inicializa a estrutura DOCS em um repositorio. E uma skill de uso unico e orienta o agente a remove-la depois da primeira execucao bem-sucedida.
- `$docs-executor`
  - Orienta execucao de planos e subplanos ja definidos.
- `$docs-plan-ap`
  - Cria Architecting Plans para mudancas com impacto arquitetural ou multiplas frentes.
- `$docs-plan-sddr`
  - Cria fluxos SDDR para mudancas locais, pequenas ou bem delimitadas.
- `$docs-reviewer`
  - Revisa coerencia estrutural, aderencia ao metodo e qualidade dos artefatos.

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
|   |-- docs-plan-ap/
|   |-- docs-plan-sddr/
|   `-- docs-reviewer/
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
