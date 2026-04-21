# database-documentation

## Objetivo
- Documentacao operacional completa da base de dados no metodo DOCS, com cobertura para bancos relacionais, NoSQL, grafos e key-value.

## Skills recomendadas
Use estas skills para exploracao, modelagem e documentacao de banco de dados.

1. `aj-geddes/useful-ai-prompts@database-schema-documentation`
- Valida porque: e focada diretamente em documentar schema e estrutura de dados.
- Use quando: voce precisa criar documentacao de tabelas, campos, constraints e relacoes.
- Instalar: `npx skills add aj-geddes/useful-ai-prompts@database-schema-documentation`

2. `langchain-ai/deepagents@schema-exploration`
- Valida porque: e especializada em exploracao de schema e descoberta estrutural.
- Use quando: voce esta analisando uma base legada antes de documentar.
- Instalar: `npx skills add langchain-ai/deepagents@schema-exploration`

3. `anthropics/knowledge-work-plugins@data-exploration`
- Valida porque: e forte para explorar dados e levantar contexto analitico.
- Use quando: voce precisa entender dominios e uso real dos dados para documentacao.
- Instalar: `npx skills add anthropics/knowledge-work-plugins@data-exploration`

4. `planetscale/database-skills@postgres`
- Valida porque: e especializada em PostgreSQL.
- Use quando: o plano envolve banco relacional com foco em Postgres.
- Instalar: `npx skills add planetscale/database-skills@postgres`

5. `aj-geddes/useful-ai-prompts@nosql-database-design`
- Valida porque: aborda modelagem/documentacao para bancos NoSQL.
- Use quando: voce precisa definir colecoes, agregados e padroes de acesso.
- Instalar: `npx skills add aj-geddes/useful-ai-prompts@nosql-database-design`

6. `personamanagmentlayer/pcl@mongodb-expert`
- Valida porque: e especializada em MongoDB.
- Use quando: a base e MongoDB e voce precisa documentar estrutura e consultas.
- Instalar: `npx skills add personamanagmentlayer/pcl@mongodb-expert`

7. `martinholovsky/claude-skills-generator@graph-database-expert`
- Valida porque: tem foco em bancos de grafos.
- Use quando: voce precisa modelar/documentar nos, arestas e propriedades.
- Instalar: `npx skills add martinholovsky/claude-skills-generator@graph-database-expert`

8. `lammesen/skills@redis-expert`
- Valida porque: e especializada em Redis e padroes key-value/cache.
- Use quando: voce precisa documentar cache, TTL, invalidacao e estruturas Redis.
- Instalar: `npx skills add lammesen/skills@redis-expert`

## Instalacao em lote (opcional)
Para disponibilizar tudo de uma vez:

```bash
npx skills add aj-geddes/useful-ai-prompts@database-schema-documentation
npx skills add langchain-ai/deepagents@schema-exploration
npx skills add anthropics/knowledge-work-plugins@data-exploration
npx skills add planetscale/database-skills@postgres
npx skills add aj-geddes/useful-ai-prompts@nosql-database-design
npx skills add personamanagmentlayer/pcl@mongodb-expert
npx skills add martinholovsky/claude-skills-generator@graph-database-expert
npx skills add lammesen/skills@redis-expert
```

## Como navegar
- `references/database-documentation/README.md`: referencia oficial de skills para documentacao de databases no DOCS.
- `utilities/skills/database-skills.md`: utilitario com comandos prontos para instalacao e verificacao.
- `references/api-documentations/README.md`: referencia complementar para documentacao e validacao de APIs.
