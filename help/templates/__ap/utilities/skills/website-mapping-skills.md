# website-mapping-skills

Lista utilitaria de skills para mapear e documentar sites a partir de URL no metodo DOCS.

## Skills recomendadas (valor e quando usar)

1. `firecrawl/cli@firecrawl`
   - Valor: melhor opcao geral para crawl de sites por URL, extraindo estrutura e conteudo em escala.
   - Quando usar: discovery inicial completo de um dominio, inventario de paginas e base para documentacao.
2. `mindmorass/reflex@site-crawler`
   - Valor: foco direto em crawling de site para mapeamento de paginas e links.
   - Quando usar: quando precisa de rastreamento objetivo da arquitetura de navegacao.
3. `leobrival/serum-plugins-official@website-crawler`
   - Valor: variante dedicada a crawler de website com abordagem pragmatica.
   - Quando usar: para alternativa leve ao fluxo principal de crawl.
4. `johnlindquist/claude@spider`
   - Valor: skill de spidering para navegar e coletar dados de paginas conectadas.
   - Quando usar: em investigacao de fluxo entre paginas e cobertura de links internos.
5. `nimbleway/agent-skills@nimble-web-tools`
   - Valor: conjunto de ferramentas web util para coleta e analise de conteudo de sites.
   - Quando usar: quando alem do mapeamento voce precisa enriquecer a analise de conteudo.
6. `aj-geddes/useful-ai-prompts@information-architecture`
   - Valor: transforma o mapeamento em estrutura de informacao documentavel.
   - Quando usar: apos crawl, para organizar hierarquia, secoes e navegacao em documentacao.
7. `agricidaniel/claude-seo@seo-sitemap`
   - Valor: apoio para visao de sitemap e cobertura estrutural do site.
   - Quando usar: para validar completude do mapa de paginas e lacunas de estrutura.

## Melhor skill (recomendada)

- `firecrawl/cli@firecrawl`
- Motivo: maior adocao entre as encontradas e aderencia direta ao caso de mapear sites por URL para posterior documentacao.

## Instalacao individual

```bash
npx skills add firecrawl/cli@firecrawl
npx skills add mindmorass/reflex@site-crawler
npx skills add leobrival/serum-plugins-official@website-crawler
npx skills add johnlindquist/claude@spider
npx skills add nimbleway/agent-skills@nimble-web-tools
npx skills add aj-geddes/useful-ai-prompts@information-architecture
npx skills add agricidaniel/claude-seo@seo-sitemap
```

## Instalacao global (usuario)

```bash
npx skills add firecrawl/cli@firecrawl -g -y
npx skills add mindmorass/reflex@site-crawler -g -y
npx skills add leobrival/serum-plugins-official@website-crawler -g -y
npx skills add johnlindquist/claude@spider -g -y
npx skills add nimbleway/agent-skills@nimble-web-tools -g -y
npx skills add aj-geddes/useful-ai-prompts@information-architecture -g -y
npx skills add agricidaniel/claude-seo@seo-sitemap -g -y
```

## Referencias

- https://skills.sh/firecrawl/cli/firecrawl
- https://skills.sh/mindmorass/reflex/site-crawler
- https://skills.sh/leobrival/serum-plugins-official/website-crawler
- https://skills.sh/johnlindquist/claude/spider
- https://skills.sh/nimbleway/agent-skills/nimble-web-tools
- https://skills.sh/aj-geddes/useful-ai-prompts/information-architecture
- https://skills.sh/agricidaniel/claude-seo/seo-sitemap

## Verificacao

```bash
npx skills check
```
