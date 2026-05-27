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

---

Tabela G_SELO_LIVRO

model: `api/packages/v1/administrativo/model/g_selo_livro.py`

---

Tabela G_EMOLUMENTO_PERIODO

model: `api/packages/v1/administrativo/model/g_emolumento_periodo.py`

---

Tabela G_EMOLUMENTO

model: `api/packages/v1/administrativo/model/g_emolumento.py`

---

Tabela G_EMOLUMENTO_ITEM

model: `api/packages/v1/administrativo/model/g_emolumento_item.py`

---