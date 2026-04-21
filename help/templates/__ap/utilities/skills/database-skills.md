# database-skills

Lista utilitaria de skills para exploracao e documentacao de databases no metodo DOCS.

## Skills e utilidade

1. `aj-geddes/useful-ai-prompts@database-schema-documentation`
   - Utilidade: acelera documentacao de tabelas, campos e relacionamentos.
   - Quando usar: quando precisa transformar schema tecnico em documentacao clara.
2. `langchain-ai/deepagents@schema-exploration`
   - Utilidade: facilita exploracao estruturada de schemas grandes.
   - Quando usar: em discovery inicial de bancos legados ou complexos.
3. `anthropics/knowledge-work-plugins@data-exploration`
   - Utilidade: apoia analise exploratoria de dados para entender comportamento real.
   - Quando usar: para investigar qualidade de dados, padroes e anomalias.
4. `planetscale/database-skills@postgres`
   - Utilidade: traz praticas especificas para PostgreSQL.
   - Quando usar: quando o banco principal e Postgres e precisa de orientacao especializada.
5. `aj-geddes/useful-ai-prompts@nosql-database-design`
   - Utilidade: orienta modelagem e decisoes de design em NoSQL.
   - Quando usar: ao definir colecoes/documentos e estrategia de acesso.
6. `personamanagmentlayer/pcl@mongodb-expert`
   - Utilidade: suporte tecnico para boas praticas e modelagem em MongoDB.
   - Quando usar: em revisao de colecoes, indices e consultas Mongo.
7. `martinholovsky/claude-skills-generator@graph-database-expert`
   - Utilidade: orienta modelagem e consultas em bancos de grafo.
   - Quando usar: em cenarios de relacoes complexas (recomendacao, fraude, redes).
8. `lammesen/skills@redis-expert`
   - Utilidade: ajuda no uso correto de Redis para cache, fila e dados temporarios.
   - Quando usar: em tuning de performance, estrategias de expiracao e padroes de cache.

## Instalacao individual

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

## Instalacao global (usuario)

```bash
npx skills add aj-geddes/useful-ai-prompts@database-schema-documentation -g -y
npx skills add langchain-ai/deepagents@schema-exploration -g -y
npx skills add anthropics/knowledge-work-plugins@data-exploration -g -y
npx skills add planetscale/database-skills@postgres -g -y
npx skills add aj-geddes/useful-ai-prompts@nosql-database-design -g -y
npx skills add personamanagmentlayer/pcl@mongodb-expert -g -y
npx skills add martinholovsky/claude-skills-generator@graph-database-expert -g -y
npx skills add lammesen/skills@redis-expert -g -y
```

## Verificacao

```bash
npx skills check
```
