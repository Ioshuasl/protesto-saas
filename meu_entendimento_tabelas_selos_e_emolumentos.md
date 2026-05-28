Tabela G_SELO_GRUPO

model: `api/packages/v1/administrativo/model/g_selo_grupo.py`

Armazena os selos da tabela de emolumentos 
- SELO_GRUPO_ID: PK
- DESCRICAO: descrição do selo (usado para identificação)
- NUMERO: código do selo (usado para identificação)
- SITUACAO: A para ativo e I para inativo
- TIPO_CARTORIO: 1 = tabelionato de notas, 2 = registro de imóveis, 3 = registro civil, 4 = registro de titulos e documentos, 5 = tabelionato de protesto
- DESCRICAO_COMPLETA: descrição do selo (praticamente o mesmo valor que DESCRICAO)
- AGRUPADOR: S caso o selo é agrupador, N ou null ou vazo caso o selo não é agrupador

---

Tabela G_SELO_LOTE

model: `api/packages/v1/administrativo/model/g_selo_lote.py`

Armazena os lotes de selos recebidos pela corregedoria
- SELO_LOTE_ID: PK
- SITUACAO: R para lote redimensionado
- DATA_LOTE: data que o lote foi importado
- NUMERO_INCIAL: numero inicial do selo do lote
- NUMERO_FINAL: numero final do selo do lote
- OBSERVACAO: texto de observação
- SELO_GRUPO_ID: FK referente a G_SELO_GRUPO
- SIGLA: numero base do selo (sem os ultimos 4 digitos)
- NOTA_FISCAL: referente a nota fiscal (por enquanto desconsiderar)
- QUANTIDADE: quantidade de selos no lote
- NUMERO_SELO_PRENOTACAO: referente ao registro de imóveis (regra de negócio)

---

Tabela G_SELO_LIVRO

model: `api/packages/v1/administrativo/model/g_selo_livro.py`

Armazena cada selo individualmente do lote de selo de G_SELO_LOTE
- SELO_LIVRO_ID: PK
- NUMERO: numeração do selo no lote
- SELO_SITUACAO_ID: FK referente a tabela G_SELO_SITUACAO (1 para aguardando a ser utilizado, 2 para utilizado, 3 para extraviado, 4 para inutilizado/cancelado, 5 para redimensionado)
- OBSERVACAO: observacao do selo
- SELO_LOTE_ID: FK referente a G_SELO_LOTE "indica em qual lote de selo esse selo pertence"
- SIGLA: numero base do selo
- DESCRICAO: descricao de atividade do selo
- TABELA: tabela que esse selo foi vinculado
- CAMPO_ID: PK da tabela que esse selo foi vinculado
- USUARIO_ID: FK para G_USUARIO
- DATA_INFORMACAO: data que o selo foi utilizado ou redimensionado
- NUMERO_AGRUPADOR: número do selo agrupador
- APRESENTANTE: nome do apresentante
- VALOR_TOTAL: valor total do selo
- VALOR_EMOLUMENTO: valor do emolumento
- VALOR_TAXA_JUDICIARIA: valor da taxa judiciaria
- DATA_EXPORTACAO: data que o selo foi exportado para a corregedoria
- CODIGO_EXPORTACAO: codigo de exportação
- DATA_CADASTRO: data que esse selo foi cadastrado
- VALOR_ISS: valor do ISS
- NUMERO_SELO: numero completo do selo

---

TABELA G_SELO_SITUACAO

model: ainda não foi criado

Tabela de dominio para mostrar a situação do selo
- SELO_SITUACAO-ID: PK
- DESCRICAO: descrição da situação do selo
- SITUACAO: A para ativo, I ou NULL para inativo

---

Tabela G_EMOLUMENTO_PERIODO

model: `api/packages/v1/administrativo/model/g_emolumento_periodo.py`

A tabela de emolumentos é atualizada de forma anual, essa tabela G_EMOLUMENTO_PERIODO serve justamente pra conseguirmos agrupar os emolumentos de G_SELO_GRUPO, G_EMOLUMENTO e G_EMOLUMENTO_ITEM agrupado pelo período
- EMOLUMENTO_PERIODO_ID: PK
- DESCRICAO: descricao do periodo da tabela de emolumento (usado para identificação visual)
- SITUACAO: A para ativo, I ou null para inativo
- DATA_INICIAL: data em que esse período passará a ser utilizado pela corregedoria

---

Tabela G_EMOLUMENTO

model: `api/packages/v1/administrativo/model/g_emolumento.py`

---

Tabela G_EMOLUMENTO_ITEM

model: `api/packages/v1/administrativo/model/g_emolumento_item.py`

---