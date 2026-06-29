# frontend-skills

Lista utilitaria de skills para frontend no metodo DOCS.

## Skills recomendadas (valor e quando usar)

1. `anthropics/skills@frontend-design`
   - Valor: gera interfaces mais consistentes, com foco em UX, layout e qualidade visual.
   - Quando usar: criacao de novas telas, redesign ou refatoracao visual de paginas.
2. `samhvw8/dot-claude@ui-design-system`
   - Valor: ajuda a estruturar design system e componentes reutilizaveis.
   - Quando usar: padronizacao de UI, bibliotecas de componentes e tokens de design.
3. `addyosmani/web-quality-skills@performance`
   - Valor: guia praticas de performance web com alto impacto em Core Web Vitals.
   - Quando usar: auditoria de lentidao, bundle grande, interacao lenta e tuning de carregamento.
4. `am-will/codex-skills@vercel-react-best-practices`
   - Valor: aplica boas praticas React/Next.js de engenharia da Vercel.
   - Quando usar: revisao tecnica de componentes, data fetching e arquitetura React/Next.
5. `josiahsiegel/claude-plugin-marketplace@tailwindcss-accessibility`
   - Valor: reforca acessibilidade em interfaces Tailwind.
   - Quando usar: projetos com TailwindCSS que precisam de melhor contraste, foco e navegacao por teclado.
6. `sergiodxa/agent-skills@frontend-testing-best-practices`
   - Valor: melhora cobertura e qualidade de testes front-end.
   - Quando usar: criacao ou revisao de testes de componentes, fluxos e regressao de UI.
7. `mindrally/skills@nextjs-react-typescript`
   - Valor: acelera setup e padroes para stack Next.js + React + TypeScript.
   - Quando usar: bootstrap de projetos ou padronizacao de projetos existentes nessa stack.
8. `existential-birds/beagle@shadcn-code-review`
   - Valor: revisao direcionada para uso de shadcn e qualidade de componentes.
   - Quando usar: repositorios com shadcn/ui em fase de crescimento ou refatoracao.
9. `yonatangross/orchestkit@radix-primitives`
   - Valor: orienta uso de primitives Radix com melhor composicao e acessibilidade.
   - Quando usar: implementacao de componentes base (dialog, menu, popover, tabs).
10. `sickn33/antigravity-awesome-skills@radix-ui-design-system`
    - Valor: combina Radix e design system para escalabilidade de UI.
    - Quando usar: arquitetura de componentes em produtos com multiplas telas.

## Instalacao individual

```bash
npx skills add anthropics/skills@frontend-design
npx skills add samhvw8/dot-claude@ui-design-system
npx skills add addyosmani/web-quality-skills@performance
npx skills add am-will/codex-skills@vercel-react-best-practices
npx skills add josiahsiegel/claude-plugin-marketplace@tailwindcss-accessibility
npx skills add sergiodxa/agent-skills@frontend-testing-best-practices
npx skills add mindrally/skills@nextjs-react-typescript
npx skills add existential-birds/beagle@shadcn-code-review
npx skills add yonatangross/orchestkit@radix-primitives
npx skills add sickn33/antigravity-awesome-skills@radix-ui-design-system
```

## Instalacao global (usuario)

```bash
npx skills add anthropics/skills@frontend-design -g -y
npx skills add samhvw8/dot-claude@ui-design-system -g -y
npx skills add addyosmani/web-quality-skills@performance -g -y
npx skills add am-will/codex-skills@vercel-react-best-practices -g -y
npx skills add josiahsiegel/claude-plugin-marketplace@tailwindcss-accessibility -g -y
npx skills add sergiodxa/agent-skills@frontend-testing-best-practices -g -y
npx skills add mindrally/skills@nextjs-react-typescript -g -y
npx skills add existential-birds/beagle@shadcn-code-review -g -y
npx skills add yonatangross/orchestkit@radix-primitives -g -y
npx skills add sickn33/antigravity-awesome-skills@radix-ui-design-system -g -y
```

## Verificacao

```bash
npx skills check
```
