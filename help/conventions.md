================================================================================
CONVENTIONS - DOCS
Regras canonicas do metodo
================================================================================

Este arquivo define as regras obrigatorias do DOCS.

Tudo o que esta descrito aqui e:
  - normativo
  - nao opcional
  - valido para humanos e agentes

================================================================================
VERDADE DO SISTEMA
================================================================================

Hierarquia oficial de verdade:
  1. codigo vivo
  2. plano, subplano ou sddd relevante
  3. references/ como indice e apoio global
  4. historico restante

Regras:
  - `references/` nao substitui plano nem codigo
  - plano historico nao vira contexto vivo automaticamente
  - contexto vivo deve continuar no melhor ponto de manutencao
  - help/ define metodo, nao estado real de execucao

================================================================================
PADROES DE NOMENCLATURA
================================================================================

PASTAS:
  - sempre em minusculo
  - kebab-case
  - sem espacos
  - sem acentos

EXCECAO:
  - a pasta raiz pode se chamar DOCS-Engenharia-de-Contexto

SUFIXOS OFICIAIS:
  - __ap
  - __sddr
  - __sp

ETAPAS INTERNAS DE SUBPLANO:
  - 01-sddd
  - 02-sddd
  - 03-sddd
  - etc

================================================================================
ESTRUTURA DE REFERENCES
================================================================================

A raiz de references/ deve conter:

  - README.md
  - global/
  - history/
  - _generated/

Regras:
  - nenhum artefato de referencia deve ficar solto na raiz, exceto README.md
  - global/ guarda somente documentos realmente repo-wide
  - history/ guarda indices historicos e tombstones
  - _generated/ guarda o indice canonico, o espelho humano gerado e a auditoria global
  - references/ nao deve duplicar contexto que ja vive melhor em plano, subplano ou sddd

================================================================================
ARQUIVOS CANONICOS
================================================================================

INDICE OFICIAL:
  - references/_generated/context-registry-bootstrap.json
  - references/_generated/context-registry.json
  - references/_generated/context-registry-for-humans/

HISTORICO INDEXADO:
  - references/history/abandoned-index.md

SDDR raiz:
  - prd.md
  - spec.md
  - status.md
  - reports/
  - references/agent-audit/
  - dependencies.md quando houver dependencia explicita

AP raiz:
  - architecting-plan/
  - final-reports/
  - status.md
  - references/agent-audit/
  - subplanos NN-...__sp/

SUBPLANO AP:
  - status.md
  - reports/
  - 01-sddd/

CADA xx-sddd:
  - prd.md
  - spec.md
  - dependencies.md

================================================================================
ESTRUTURA OBRIGATORIA
================================================================================

Todo plano deve estar em exatamente um dos caminhos:

  - plans-to-be-executed/
  - plans-executed/
  - plans-abandoned/

Nunca em ambos.

Regras para plans-abandoned/:
  - e historico imutavel
  - nao deve ser retomado no mesmo diretorio
  - retomada exige novo plano em PTBE
  - se houver valor residual, ele deve ser indexado em references/history/abandoned-index.md

Regras para AP:
  - nao existe mais backup-plans/
  - todo subplano deve nascer com 01-sddd/
  - 02-sddd/ e seguintes so surgem quando a etapa anterior nao cobre o trabalho
  - reports ficam na raiz do subplano, nao dentro do xx-sddd

Regras para SDDR:
  - SDDR nao usa xx-sddd
  - SDDR fica na raiz do plano, nao em subetapas internas artificiais

================================================================================
STATUS
================================================================================

Todo plano e subplano deve possuir status.md.

Estados oficiais:
  - draft
  - ready
  - running
  - blocked
  - completed

Sem status.md nao existe execucao valida.

No subplano AP:
  - o status oficial e sempre o status.md da raiz do __sp

================================================================================
DEPENDENCIAS
================================================================================

Dependencias devem ser explicitas.

Regras:
  - dependencies.md e obrigatorio em cada xx-sddd
  - dependencies.md e obrigatorio em SDDR quando houver dependencia

Dependencia implicita e erro de metodo.

================================================================================
REPORTS
================================================================================

Todo plano executado deve gerar relatorios.

Relatorios sao a base de:
  - prova de execucao
  - transferencia de contexto
  - historico tecnico

No subplano AP:
  - reports/ da raiz documenta o que foi executado nos xx-sddd
  - reports/ da raiz registra handoffs do subplano

Arquivo existente, mas incompleto, nao satisfaz o metodo.

================================================================================
INITS OFICIAIS
================================================================================

A unica raiz oficial de inits e:
  - help/inits/init-agents/

Conjunto oficial:
  - init-plan-ap-agent.md
  - init-plan-sddr-agent.md
  - init-executor-agent.md
  - init-reviewer-agent.md

Regras:
  - nao existe mais init-bootstrap-agent.md como init oficial
  - o bootstrap foi absorvido por init-executor-agent.md
  - nao existe mais help/inits/init-plans/
  - init de planner nao substitui init de executor
  - init de reviewer nao e init de code review de produto

================================================================================
PROMOCAO PARA REFERENCES
================================================================================

references/ nao substitui planos nem subplanos.

So deve haver promocao para references/ quando a informacao for:

  - repo-wide
  - realmente global
  - melhor consumida fora do plano original

Exemplos validos:
  - identidade atual do sistema
  - contratos globais usados por multiplas frentes
  - indice historico residual

Saidas geradas oficiais:
  - references/_generated/context-registry.json
  - references/_generated/context-registry-for-humans/
  - references/_generated/agent-audit/

================================================================================
AUDITORIA DE AGENTE
================================================================================

Gavetas oficiais:
  - global: references/_generated/agent-audit/
  - por plano: <plano>/references/agent-audit/

Formato canonico por execucao:
  - YYYY-MM-DD__agent-role__slug/

Arquivos minimos por execucao:
  - run.md
  - artifacts/ (opcional)

Regra:
  - handoff nao fica em agent-audit
  - handoff fica em reports/ ou na resposta final do agente

================================================================================
DEFINITION OF DONE (DoD)
================================================================================

Um plano so pode ser considerado concluido quando:

  - todos os contratos foram cumpridos
  - dependencias foram resolvidas
  - relatorios obrigatorios existem e estao completos
  - status.md indica completed

So apos isso o plano pode sair de plans-to-be-executed/.

================================================================================
ANTIPADROES
================================================================================

X tratar plano historico como contexto vivo sem promocao especifica
X usar references/ para duplicar o que ja esta melhor explicado em subplano ou sddd
X criar backup-plans/ em AP
X colocar reports dentro de xx-sddd
X abrir 02-sddd/ antes de 01-sddd/ existir
X assumir dependencia implicita
X manter bootstrap como init paralelo ao executor
X gravar handoff em agent-audit
X usar `references/` para recontar contexto que continua melhor no plano
X abrir bootstrap lendo registry completo por padrao

================================================================================
FIM DO conventions.md
================================================================================
