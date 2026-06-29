# DOCS - ENGENHARIA DE CONTEXTO

**Documentacao Oficial do Metodo**  
By JG

## Visao Geral

DOCS e um metodo de Engenharia de Contexto para Programacao Orientada por IA.

Ele define como o contexto deve ser:
- estruturado
- versionado
- distribuido
- executado
- preservado

O objetivo do DOCS e permitir que agentes de IA e humanos executem mudancas em sistemas de software de forma previsivel, rastreavel e controlada.

No DOCS, documentacao nao e um subproduto.  
Documentacao e **INFRAESTRUTURA OPERACIONAL**.

## O Problema Que o DOCS Resolve

Agentes de IA nao possuem memoria persistente confiavel.  
Cada execucao depende exclusivamente do contexto fornecido.

Sem um metodo:
- decisoes se perdem
- trabalho e refeito
- conflitos surgem
- historico desaparece
- auditoria se torna impossivel

O DOCS resolve isso externalizando memoria, estado e decisoes em uma estrutura de documentacao rigorosa.

## Principios Fundamentais

1. **CONTEXTO COMO INFRAESTRUTURA**  
   Tudo o que nao esta documentado nao existe para execucao.
2. **DOCUMENTACAO COMO CONTRATO**  
   Arquivos `.md` nao explicam: eles delimitam o que pode e nao pode ser feito.
3. **DEPENDENCIAS EXPLICITAS**  
   Nada e implicito. Dependencia nao documentada e erro de metodo.
4. **GOVERNANCA DE ESTADO**  
   Todo plano possui estado explicito (`status.md`).
5. **MEMORIA PERSISTENTE**  
   Historico vive fora da IA, em estrutura versionada.

## Estrutura Geral do DOCS

```text
DOCS-Engenharia-de-Contexto/
├── README.md
├── help/
├── plans-to-be-executed/
├── plans-executed/
├── plans-abandoned/
└── web/ (aplicacao frontend do metodo)
```

Cada pasta possui um papel especifico no metodo.

## Pasta `help/`

A pasta `help/` contem a **DOCUMENTACAO DO METODO**.

Ela:
- explica o DOCS
- define regras
- padroniza linguagem
- fornece templates

Nada em `help/` e execucao real.  
`help/` e fonte conceitual e normativa.

## Plans-to-be-executed (PTBE)

Contem todos os planos ainda nao concluidos.

E o espaco:
- ativo
- mutavel
- em execucao

Nenhum plano em PTBE e considerado verdade historica.

## Plans-executed (PE)

Contem todos os planos concluidos.

E o espaco:
- imutavel
- historico
- somente leitura

Tudo em PE e verdade consolidada do sistema.

## Plans-abandoned (PA)

Contem todos os planos interrompidos/abandonados.

E o espaco:
- imutavel
- historico
- somente leitura

PA preserva rastreabilidade de decisoes de abandono.  
Se um trabalho precisar ser retomado, um **NOVO** plano deve nascer em PTBE, referenciando explicitamente o plano abandonado.

## Caminhos de Execucao

O DOCS possui tres caminhos de execucao:

1. **AP - Architecting Plan**  
   Para problemas grandes, estruturais e complexos.
2. **SDDR - Spec-Driven Development with Reports**  
   Para problemas pequenos, locais e bem delimitados, com reports obrigatorios.
3. **AN - Analyze (`__an`) - Coming Soon!**  
   Para analise estruturada de repositorios existentes, cobrindo:
   - codigo-fonte
   - banco de dados
   - endpoints/contratos de API

Cada plano **DEVE** escolher exatamente um caminho.  
Enquanto estiver Coming Soon, AN e trilha de analise e diagnostico, sem fluxo executavel completo no metodo atual.

## AP - Architecting Plan

AP e utilizado quando:
- ha impacto arquitetural
- multiplos modulos estao envolvidos
- o trabalho precisa ser decomposto
- dependencias existem
- execucao paralela e desejavel

AP e um plano **EXECUTAVEL** e **ORQUESTRADO**.  
Ele contem subplanos que seguem o metodo **SDDDR** (Spec-Driven Development with Dependencies and Reports).

Dentro de AP, pode existir a pasta `backup-plans/` para planos de contingencia que destravam a execucao quando um subplano fica bloqueado.

Um backup-plan e um subplano especial e **DEVE** seguir SDDDR completo:
- `prd.md`
- `spec.md`
- `dependencies.md`
- `status.md`
- reports (`report-success.md` e/ou `report-merge.md`)

Apos concluir um backup-plan, e obrigatoria uma revisao de impacto:
- retroativa: subplanos passados
- prospectiva: subplanos seguintes

Essa revisao e **BLOQUEANTE**: o AP nao deve avancar sem esse registro.

## SDDR - Caminho Simples

SDDR e um metodo direto de execucao com documentacao obrigatoria.

Fluxo minimo:
1. `prd.md`
2. `spec.md`
3. execucao + report/ `report-success.md` & `report-merge.md`

SDDR prioriza velocidade com rastreabilidade.

## SDDDR - Spec-Driven Development with Dependencies and Reports (Restrito a Subplanos AP)

SDDDR e o metodo de execucao dos subplanos dentro de um AP.  
Ele existe para explicitar dependencias entre subplanos e registrar reports.

SDDDR **NAO** e um caminho independente do metodo.

## `status.md`

`status.md` governa o estado de planos e subplanos.

Sem `status.md` nao existe execucao valida.

## Definition of Done (DoD)

Um plano so e considerado concluido quando:
- todos os contratos foram cumpridos
- relatorios obrigatorios estao completos
- dependencias foram resolvidas
- `status.md` indica `completed`

No AP, a migracao de PTBE para PE exige pacote final de reports completo em `final-reports/` (mestre, anexos e checklist de gate).

## Conclusao

DOCS e um metodo para tornar o uso de IA em software previsivel, auditavel e escalavel.

Ele transforma documentacao em sistema operacional de contexto.

## Extensoes Para Documentacao de Databases e APIs

Para acelerar exploracao, documentacao e validacao no metodo DOCS, use:

### Databases
- `help/templates/__ap/references/database-documentation/README.md`  
  Catalogo de skills para exploracao e documentacao de bancos de dados.
- `help/templates/__ap/utilities/skills/database-skills.md`  
  Comandos prontos para instalar e verificar skills de databases.

### APIs
- `help/templates/__ap/references/api-documentations/README.md`  
  Catalogo de skills para exploracao, documentacao e validacao de APIs.
- `help/templates/__ap/utilities/skills/api-skills.md`  
  Comandos prontos para instalar e verificar skills de APIs.

Essas referencias sao opcionais, mas recomendadas quando o plano envolve:
- descoberta de schema de dados e contratos de API
- mapeamento de relacoes entre dominio, banco e endpoints
- documentacao tecnica para execucao por agentes
- validacao de consistencia entre implementacao e especificacao
