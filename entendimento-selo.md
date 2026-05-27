Ótima direção — esses dois SQLs deixam bem claro o vínculo de negócio entre os três models.

## Leitura do relacionamento (com base nos SQLs)

- **`G_EMOLUMENTO_PERIODO` é o “cabeçalho de vigência”**  
  Nos dois arquivos, primeiro cria/atualiza um período e depois popula vários itens usando esse mesmo ID de período.
- **`G_EMOLUMENTO_ITEM` é a tabela de faixas/regras**  
  Cada item vem com:
  - `EMOLUMENTO_PERIODO_ID` (vigência)
  - `SELO_GRUPO_ID` (grupo de selo)
  - valores por faixa (`VALOR_INICIO`, `VALOR_FIM`, `VALOR_EMOLUMENTO`, `VALOR_TAXA_JUDICIARIA` etc.)
- **`G_SELO_GRUPO` representa o ato/grupo tarifário**  
  O script de emolumentos atualiza massivamente os grupos e os itens apontam para eles por `SELO_GRUPO_ID`.

## Evidências diretas nos SQLs

```3:10:tx_judiciaria_2026_calculo_orius_trigger_corrigida.SQL
--Criando o Emolumento_Periodo
UPDATE OR INSERT INTO G_EMOLUMENTO_PERIODO (EMOLUMENTO_PERIODO_ID, DESCRICAO, SITUACAO, DATA_INICIAL)
                                    VALUES (50032, 'Tabela Taxa Judiciária 2026 GO', 'A', '2026-02-01 00:00:00');COMMIT WORK;

UPDATE OR INSERT INTO G_EMOLUMENTO_ITEM (..., EMOLUMENTO_PERIODO_ID, ..., SELO_GRUPO_ID, ...)
                                 VALUES (..., 50032, ..., 46451, ...)
```

```2:8:Emolumentos_2026.sql
--Criando o Emolumento_Periodo
UPDATE OR INSERT INTO G_EMOLUMENTO_PERIODO (EMOLUMENTO_PERIODO_ID, DESCRICAO, SITUACAO, DATA_INICIAL)
                                    VALUES (50031, 'Tabela Emolumento 2026 GO', 'A', '2026-01-01 00:00:00');COMMIT WORK;

--Selo Grupo (aqui trocamos a descrição dos grupos de selo)
UPDATE OR INSERT INTO G_SELO_GRUPO (...)
```

## Conclusão para os models

- Relação **forte e correta**:
  - `G_EMOLUMENTO_PERIODO (1) -> (N) G_EMOLUMENTO_ITEM`
  - `G_SELO_GRUPO (1) -> (N) G_EMOLUMENTO_ITEM`
- Isso está totalmente alinhado com o que você estruturou no `index.py`.
- O fluxo de negócio implícito é: **vigência (`periodo`) + ato (`selo_grupo`) => faixa/regra (`emolumento_item`)**.

Se quiser, no próximo passo eu monto uma query de validação (ORM + SQL) para provar em runtime: “quantos itens por período” e “quantos itens por grupo de selo” usando os IDs `50031` e `50032`.

## Consultas com include (validadas)

### 1) Item com include de grupo de selo

```python
from packages.v1.administrativo.model.index import register_administrativo_associations
from packages.v1.administrativo.model.g_emolumento_item import get_g_emolumento_item_model
from packages.v1.administrativo.model.g_selo_grupo import get_g_selo_grupo_model

register_administrativo_associations()

G_EMOLUMENTO_ITEM = get_g_emolumento_item_model()
G_SELO_GRUPO = get_g_selo_grupo_model()

rows = G_EMOLUMENTO_ITEM.findAll(
    {
        "include": [{"model": G_SELO_GRUPO, "as": "selo_grupo", "required": False}],
        "limit": 3,
        "order": [("EMOLUMENTO_ITEM_ID", "DESC")],
    }
)
```

Comportamento observado: os registros vieram com `selo_grupo` preenchido para os itens amostrados (incluindo `DESCRICAO` do grupo).

### 2) Período com include de itens

```python
from packages.v1.administrativo.model.index import register_administrativo_associations
from packages.v1.administrativo.model.g_emolumento_periodo import (
    get_g_emolumento_periodo_model,
)
from packages.v1.administrativo.model.g_emolumento_item import get_g_emolumento_item_model

register_administrativo_associations()

G_EMOLUMENTO_PERIODO = get_g_emolumento_periodo_model()
G_EMOLUMENTO_ITEM = get_g_emolumento_item_model()

rows = G_EMOLUMENTO_PERIODO.findAll(
    {
        "include": [{"model": G_EMOLUMENTO_ITEM, "as": "itens", "required": False}],
        "limit": 1,
        "order": [("EMOLUMENTO_PERIODO_ID", "DESC")],
    }
)
```

Comportamento observado: o período mais recente retornado foi `50031` e o include trouxe `itens`.

### 3) Métrica direta de volume por período (sem include)

```python
from packages.v1.administrativo.model.g_emolumento_item import get_g_emolumento_item_model

G_EMOLUMENTO_ITEM = get_g_emolumento_item_model()
total_50031 = G_EMOLUMENTO_ITEM.count({"where": {"EMOLUMENTO_PERIODO_ID": 50031}})
```

Comportamento observado: `count_50031 = 1544` (confirmando grande volume de faixas para o período 2026 carregado).

## Observações importantes para uso futuro

- Use `register_administrativo_associations()` antes de consultas com `include`.
- Para auditoria de volume, prefira `count` e listagens por `G_EMOLUMENTO_ITEM` com filtro de `EMOLUMENTO_PERIODO_ID`.
- `include` a partir de `G_EMOLUMENTO_PERIODO` pode ser útil para navegação, mas para leitura completa de todas as faixas do período, é mais confiável consultar diretamente `G_EMOLUMENTO_ITEM` filtrando por período.

## Cuidado essencial: selos agrupadores (G_SELO_GRUPO)

Para selos eletrônicos extrajudiciais, não usar apenas `SELO_GRUPO_ID` como chave de entendimento.
É obrigatório considerar também:

- `SELO_GRUPO_ID_AGRUPADOR`: vínculo hierárquico direto para um grupo agregador.
- `GRUPOS_PRINCIPAL`: lista lógica de números de grupos principais (ex.: `3080`) que define pertencimento funcional.

Na prática, isso impacta:

- montagem de regras de negócio para seleção/aplicação de selo;
- leitura correta de famílias de selos por grupo principal;
- filtros de tela e validações de backend (não confundir grupo individual com grupo principal).

### Esquema recomendado de consulta

#### 1) Descobrir todos os selos vinculados a um grupo principal

```sql
SELECT
    SELO_GRUPO_ID,
    NUMERO,
    DESCRICAO,
    SELO_GRUPO_ID_AGRUPADOR,
    GRUPOS_PRINCIPAL,
    TIPO_CARTORIO,
    TIPO_SELO,
    SITUACAO
FROM G_SELO_GRUPO
WHERE GRUPOS_PRINCIPAL IS NOT NULL
  AND UPPER(GRUPOS_PRINCIPAL) CONTAINING '3080'
ORDER BY NUMERO, SELO_GRUPO_ID;
```

Resultado observado: 26 selos vinculados a `GRUPOS_PRINCIPAL` contendo `3080`, com `TIPO_CARTORIO = '5'` (protesto).

#### 2) Cruzar emolumento -> item -> selo grupo (considerando principal)

```sql
SELECT DISTINCT
    e.EMOLUMENTO_ID,
    e.DESCRICAO AS EMOLUMENTO_DESCRICAO,
    i.EMOLUMENTO_ITEM_ID,
    i.SELO_GRUPO_ID,
    g.NUMERO,
    g.DESCRICAO AS SELO_DESCRICAO,
    g.SELO_GRUPO_ID_AGRUPADOR,
    g.GRUPOS_PRINCIPAL
FROM G_EMOLUMENTO e
JOIN G_EMOLUMENTO_ITEM i ON i.EMOLUMENTO_ID = e.EMOLUMENTO_ID
LEFT JOIN G_SELO_GRUPO g ON g.SELO_GRUPO_ID = i.SELO_GRUPO_ID
WHERE e.EMOLUMENTO_ID = :emolumento_id
ORDER BY i.EMOLUMENTO_ITEM_ID DESC;
```

#### 3) Regra operacional para consultas futuras

- Primeiro localize o `EMOLUMENTO_ID`.
- Depois busque os `SELO_GRUPO_ID` em `G_EMOLUMENTO_ITEM`.
- Em seguida expanda em `G_SELO_GRUPO` avaliando:
  - `SELO_GRUPO_ID_AGRUPADOR` (hierarquia),
  - `GRUPOS_PRINCIPAL` (pertencimento a famílias principais, como `3080`).