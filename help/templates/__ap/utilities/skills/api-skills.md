# api-skills

Lista utilitaria de skills para exploracao, documentacao e validacao de APIs no metodo DOCS.

## Skills e utilidade

1. `sickn33/antigravity-awesome-skills@api-documentation-generator`
   - Utilidade: acelera a geracao de documentacao tecnica de endpoints.
   - Quando usar: quando a API existe, mas falta documentacao padronizada.
2. `aj-geddes/useful-ai-prompts@api-reference-documentation`
   - Utilidade: melhora clareza de referencia (parametros, respostas, erros).
   - Quando usar: para criar guias de consulta rapida para devs e agentes.
3. `hairyf/skills@openapi-specification-v2`
   - Utilidade: orienta estrutura e qualidade de especificacoes OpenAPI.
   - Quando usar: ao escrever ou revisar contratos REST/OpenAPI.
4. `personamanagmentlayer/pcl@openapi-expert`
   - Utilidade: apoia analise tecnica avancada de contratos OpenAPI.
   - Quando usar: em revisao de consistencia entre implementacao e spec.
5. `aj-geddes/useful-ai-prompts@api-contract-testing`
   - Utilidade: ajuda a validar se implementacao respeita o contrato.
   - Quando usar: em testes de regressao de contrato e integracao.
6. `secondsky/claude-skills@api-testing`
   - Utilidade: amplia cobertura de testes funcionais de API.
   - Quando usar: antes de releases e em investigacao de bugs de endpoint.
7. `aj-geddes/useful-ai-prompts@rest-api-design`
   - Utilidade: melhora desenho de recursos, rotas e semantica HTTP.
   - Quando usar: em criacao/refatoracao de APIs REST.
8. `apollographql/skills@graphql-operations`
   - Utilidade: orienta boas praticas em operacoes GraphQL.
   - Quando usar: em APIs GraphQL com foco em queries, mutations e padroes.

## Instalacao individual

```bash
npx skills add sickn33/antigravity-awesome-skills@api-documentation-generator
npx skills add aj-geddes/useful-ai-prompts@api-reference-documentation
npx skills add hairyf/skills@openapi-specification-v2
npx skills add personamanagmentlayer/pcl@openapi-expert
npx skills add aj-geddes/useful-ai-prompts@api-contract-testing
npx skills add secondsky/claude-skills@api-testing
npx skills add aj-geddes/useful-ai-prompts@rest-api-design
npx skills add apollographql/skills@graphql-operations
```

## Instalacao global (usuario)

```bash
npx skills add sickn33/antigravity-awesome-skills@api-documentation-generator -g -y
npx skills add aj-geddes/useful-ai-prompts@api-reference-documentation -g -y
npx skills add hairyf/skills@openapi-specification-v2 -g -y
npx skills add personamanagmentlayer/pcl@openapi-expert -g -y
npx skills add aj-geddes/useful-ai-prompts@api-contract-testing -g -y
npx skills add secondsky/claude-skills@api-testing -g -y
npx skills add aj-geddes/useful-ai-prompts@rest-api-design -g -y
npx skills add apollographql/skills@graphql-operations -g -y
```

## Verificacao

```bash
npx skills check
```
