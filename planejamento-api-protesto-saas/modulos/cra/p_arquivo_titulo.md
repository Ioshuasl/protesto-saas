# PArquivoTitulo (CRA)

| Campo | Valor |
|-------|-------|
| Pacote (código) | `api/packages/v1/administrativo/` |
| Prefix HTTP | `/administrativo/p_arquivo_titulo` |
| DataConfig | `app/src/packages/cra/data/PTituloArquivo/pTituloArquivoDataConfig.ts` |
| Tabela | `P_ARQUIVO_TITULO` |
| Fase | 6 |
| Status | implementado |
| `USE_ORM_FIREBIRD` | `true` |

> Rotas em `/administrativo/p_arquivo_titulo`; código em `packages/v1/administrativo/`.

## Rotas — CRUD inicial

| Operação | Método | Path |
|----------|--------|------|
| index | GET | `/` |
| show | GET | `/{arquivo_titulo_id}/` |
| create | POST | `/` |
| update | PUT | `/{arquivo_titulo_id}/` |
| delete | DELETE | `/{arquivo_titulo_id}/` |

### Rotas — conteúdo BLOB (fora do CRUD)

Colunas `TEXTO` e `TEXTO_IMPORTADO` **não** entram em index, show, create nem update. Leitura (e gravação futura) em endpoints dedicados.

| Operação | Método | Path | Coluna |
|----------|--------|------|--------|
| show texto | GET | `/{arquivo_titulo_id}/texto/` | `TEXTO` |
| show texto importado | GET | `/{arquivo_titulo_id}/texto_importado/` | `TEXTO_IMPORTADO` |
| download arquivo | GET | `/{arquivo_titulo_id}/download/` | `TEXTO_IMPORTADO` (corpo) + `NOME_ARQUIVO` (nome do download) |

Resposta sugerida (`texto` / `texto_importado`): `{ "message", "data": { "arquivo_titulo_id", "conteudo" } }` — `conteudo` como string decodificada (zlib Febraban + ISO-8859-1).

**Download:** `Content-Disposition: attachment` com filename = `NOME_ARQUIVO`; corpo = bytes de `TEXTO_IMPORTADO` decodificado (`text/plain; charset=iso-8859-1`). 404 se registro ou BLOB ausente.

## Schema Firebird (`describe_table`)

| Coluna | Tipo | Tamanho | Nullable | API (snake_case) |
|--------|------|---------|----------|------------------|
| `ARQUIVO_TITULO_ID` | NUMERIC(10,2) | PK | não | `arquivo_titulo_id` |
| `DATA_IMPORTACAO` | TIMESTAMP | — | sim | `data_importacao` |
| `QUANTIDADE` | NUMERIC(10,2) | — | sim | `quantidade` |
| `DATA_MOVIMENTO` | VARCHAR | 30 | sim | `data_movimento` |
| `NUMERO_SEQUENCIAL` | VARCHAR | 30 | sim | `numero_sequencial` |
| `QTDE_REGISTROS` | VARCHAR | 30 | sim | `qtde_registros` |
| `QTDE_TITULOS` | VARCHAR | 30 | sim | `qtde_titulos` |
| `QTDE_INDICACOES` | VARCHAR | 30 | sim | `qtde_indicacoes` |
| `QTDE_ORIGINAIS` | VARCHAR | 30 | sim | `qtde_originais` |
| `SOMA_VLR_REMESSA` | NUMERIC(10,2) | — | sim | `soma_vlr_remessa` |
| `SOMA_QTDE_REMESSA` | NUMERIC(10,2) | — | sim | `soma_qtde_remessa` |
| `AGENCIA_CENTRALIZADORA` | VARCHAR | 10 | sim | `agencia_centralizadora` |
| `CODIGO_PRACA` | VARCHAR | 10 | sim | `codigo_praca` |
| `SEQUENCIAL_HEADER` | VARCHAR | 10 | sim | `sequencial_header` |
| `NOME_ARQUIVO` | VARCHAR | 150 | sim | `nome_arquivo` |
| `PORTADOR_NOME` | VARCHAR | 60 | sim | `portador_nome` |
| `COMPLEMENTO_HEADER` | VARCHAR | 260 | sim | `complemento_header` |
| `IDENTIFICACAO_REGISTRO` | VARCHAR | 1 | sim | `identificacao_registro` |
| `PORTADOR_CODIGO` | VARCHAR | 3 | sim | `portador_codigo` |
| `ID_TRANSACAO_REMETENTE` | VARCHAR | 3 | sim | `id_transacao_remetente` |
| `ID_TRANSACAO_DESTINATARIO` | VARCHAR | 3 | sim | `id_transacao_destinatario` |
| `ID_TRANSACAO_TIPO` | VARCHAR | 3 | sim | `id_transacao_tipo` |
| `VERSAO_LAYOUT` | VARCHAR | 3 | sim | `versao_layout` |
| `SEQUENCIAL_FOOTER` | VARCHAR | 15 | sim | `sequencial_footer` |
| `COMPLEMENTO_REGISTRO` | VARCHAR | 1000 | sim | `complemento_registro` |
| `TEXTO` | BLOB BINARY | — | sim | **somente** `GET .../texto/` |
| `TEXTO_IMPORTADO` | BLOB BINARY | — | sim | **somente** `GET .../texto_importado/` |

### FKs relevantes

| FK | Filho | Pai |
|----|-------|-----|
| `P_TITULO_P_ARQUIVO_TITULO_FK` | `P_TITULO.ARQUIVO_TITULO_ID` | `P_ARQUIVO_TITULO.ARQUIVO_TITULO_ID` |
| `P_FEBRABAN_CABECALHO_P_ARQU_FK` | `P_FEBRABAN_CABECALHO.ARQUIVO_TITULO_ID` | `P_ARQUIVO_TITULO` |
| `P_FEBRABAN_DETALHE_P_ARQUIV_FK` | `P_FEBRABAN_DETALHE.ARQUIVO_TITULO_ID` | `P_ARQUIVO_TITULO` |
| `P_FEBRABAN_RODAPE_P_ARQUIVO_FK` | `P_FEBRABAN_RODAPE.ARQUIVO_TITULO_ID` | `P_ARQUIVO_TITULO` |

## Amostra (10 registros — `santarita`, ordem `ARQUIVO_TITULO_ID DESC`)

Total na base: **1810** arquivos.

| arquivo_titulo_id | data_importacao | nome_arquivo | portador_codigo | quantidade | soma_vlr_remessa (banco) | soma_vlr_remessa (API) | data_movimento |
|-------------------|-----------------|--------------|-----------------|------------|--------------------------|------------------------|----------------|
| 302735 | 2025-10-28 17:30 | B7562210.251 | 756 | 1 | 117123 | 1171.23 | 22102025 |
| 302734 | 2025-10-28 17:28 | B7482810.251 | 748 | 1 | 50000 | 500.00 | 28102025 |
| 302732 | 2025-10-28 17:21 | B0332710.251 | 033 | 2 | 103449 | 1034.49 | 27102025 |
| 302731 | 2025-10-28 17:16 | B3412710.251 | 341 | 1 | 112800 | 1128.00 | 27102025 |

### Valores distintos (amostra / tabela)

| Coluna | Valores observados |
|--------|-------------------|
| `ID_TRANSACAO_DESTINATARIO` | `SDT` |
| `ID_TRANSACAO_TIPO` | `TPR` |
| `VERSAO_LAYOUT` | `043` |
| `IDENTIFICACAO_REGISTRO` | `9` |
| `ID_TRANSACAO_REMETENTE` | `NULL` (amostra) |
| `TEXTO` | sempre `NULL` na amostra |
| `TEXTO_IMPORTADO` | BLOB presente (~850–1300 bytes) |

### Serialização monetária

`SOMA_VLR_REMESSA` no Firebird está em **centavos** (ex.: `117123` ↔ `P_TITULO.VALOR_TITULO = 1171.23` para o mesmo `arquivo_titulo_id`). Na API: **÷ 100** na saída; **× 100** na entrada (create/update).

`DATA_MOVIMENTO`: string `DDMMYYYY` no banco (ex. `22102025`); API pode expor como string ou `YYYY-MM-DD` parseado — alinhar ao mock (`2026-04-15`).

`QTDE_*`: strings zero-padded do layout Febraban (`0001`, `0002`); expor como string na API.

## Siglas API

Não há coluna `SITUACAO`. Campos `VARCHAR(1)` / códigos Febraban — expor valor do banco como string (sem mapa de siglas adicional nesta fase), salvo confirmação futura.

| Coluna | Tratamento API |
|--------|----------------|
| `IDENTIFICACAO_REGISTRO` | string literal (`9` = trailer no layout) |
| `ID_TRANSACAO_*` | string literal (`TPR`, `SDT`, …) |
| `VERSAO_LAYOUT` | string literal (`043`) |

## Regras de negócio — CRUD inicial

- **index**: formato3 (`p`, `per_page`, `sort`); **sem** colunas BLOB; resposta com `pagination`. Opcional `?include=titulos` retorna `titulos: [{ "numero_apontamento": … }]` (somente `NUMERO_APONTAMENTO` de `P_TITULO`, via `hasMany` ORM ou batch SQL).
- **show**: metadados do arquivo; **sem** BLOB; opcional `?include=titulos` (títulos completos via `map_titulo_row`).
- **create/update**: body sem `texto` / `texto_importado`; `arquivo_titulo_id` via `G_SEQUENCIA` / `GenerateService` tabela `P_ARQUIVO_TITULO` no create.
- **delete**: físico; bloquear **409** se existir `P_TITULO` com `ARQUIVO_TITULO_ID` (e/ou registros `P_FEBRABAN_*` — confirmar na implementação).
- **BLOB**: apenas leitura nos endpoints dedicados; upload/update de BLOB fica para fase seguinte.

## Index formato3

| Item | Valor |
|------|--------|
| PK (fallback sort) | `arquivo_titulo_id` |
| Campos sort | `arquivo_titulo_id`, `data_importacao`, `nome_arquivo`, `portador_codigo`, `quantidade`, `soma_vlr_remessa` |
| Filtros negócio (`IndexSchema`) | `nome_arquivo`, `portador_codigo` (= `P_BANCO.CODIGO_BANCO`), `codigo_praca`, `data_inicio` / `data_fim` (intervalo em `DATA_IMPORTACAO`) |
| Paginação resposta | sim |
| Postman All | `?p=1&per_page=20&sort=arquivo_titulo_id.desc&...` |
| Include (opcional) | `?include=titulos` → `titulos[].numero_apontamento` |

Separação endpoint: `_P_ARQUIVO_TITULO_INDEX_FILTER_KEYS` — sem `p`, `per_page`, `sort`, `f`, `include`.

## Models necessários (inventário)

| Tabela | Arquivo | Motivo | Status |
|--------|---------|--------|--------|
| `P_ARQUIVO_TITULO` | `model/p_arquivo_titulo.py` | Entidade alvo | **criado** |
| `P_TITULO` | `model/p_titulo.py` | FK delete / show futuro | existe |

### Associações planejadas (`model/index.py`)

| Origem | Tipo | Destino | FK | `as` |
|--------|------|---------|-----|------|
| `P_ARQUIVO_TITULO` | `hasMany` | `P_TITULO` | `ARQUIVO_TITULO_ID` em `P_TITULO` | `titulos` |

`register_administrativo_associations()` — `titulos` registrado; usado no index (`NUMERO_APONTAMENTO` only) e show (título completo).

## Arquivos (matriz — `packages/v1/administrativo/`)

Prefixo de caminhos: `api/packages/v1/administrativo/`.

| # | Camada | Arquivo |
|---|--------|---------|
| 1 | model | `model/p_arquivo_titulo.py` |
| 2 | schema | `schemas/p_arquivo_titulo_schema.py` |
| 3 | repository | `repositories/p_arquivo_titulo/p_arquivo_titulo_index_repository.py` |
| 4 | repository | `repositories/p_arquivo_titulo/p_arquivo_titulo_show_repository.py` |
| 5 | repository | `repositories/p_arquivo_titulo/p_arquivo_titulo_save_repository.py` |
| 6 | repository | `repositories/p_arquivo_titulo/p_arquivo_titulo_update_repository.py` |
| 7 | repository | `repositories/p_arquivo_titulo/p_arquivo_titulo_delete_repository.py` |
| 8 | repository | `repositories/p_arquivo_titulo/p_arquivo_titulo_show_texto_repository.py` |
| 9 | repository | `repositories/p_arquivo_titulo/p_arquivo_titulo_show_texto_importado_repository.py` |
| 10 | repository | `repositories/p_arquivo_titulo/p_arquivo_titulo_count_titulo_repository.py` (delete) |
| 11 | action | `actions/p_arquivo_titulo/p_arquivo_titulo_index_action.py` |
| 12 | action | `actions/p_arquivo_titulo/p_arquivo_titulo_show_action.py` |
| 13 | action | `actions/p_arquivo_titulo/p_arquivo_titulo_save_action.py` |
| 14 | action | `actions/p_arquivo_titulo/p_arquivo_titulo_update_action.py` |
| 15 | action | `actions/p_arquivo_titulo/p_arquivo_titulo_delete_action.py` |
| 16 | action | `actions/p_arquivo_titulo/p_arquivo_titulo_show_texto_action.py` |
| 17 | action | `actions/p_arquivo_titulo/p_arquivo_titulo_show_texto_importado_action.py` |
| 18 | service | `services/p_arquivo_titulo/go/p_arquivo_titulo_index_service.py` |
| 19 | service | `services/p_arquivo_titulo/go/p_arquivo_titulo_show_service.py` |
| 20 | service | `services/p_arquivo_titulo/go/p_arquivo_titulo_save_service.py` |
| 21 | service | `services/p_arquivo_titulo/go/p_arquivo_titulo_update_service.py` |
| 22 | service | `services/p_arquivo_titulo/go/p_arquivo_titulo_delete_service.py` |
| 23 | service | `services/p_arquivo_titulo/go/p_arquivo_titulo_show_texto_service.py` |
| 24 | service | `services/p_arquivo_titulo/go/p_arquivo_titulo_show_texto_importado_service.py` |
| 25 | controller | `controllers/p_arquivo_titulo_controller.py` |
| 26 | endpoint | `endpoints/p_arquivo_titulo_endpoint.py` |
| 27 | registro | `packages/v1/api.py` |
| 28 | postman | `Orius.postman_collection.json` → `CRA` / `Arquivo Titulo` |
| 29 | test | `tests/unit/administrativo/p_arquivo_titulo/` (mínimo index + show) |

Sem `*_orm_query`, `*_codec`, `*_row_mapper` em `repositories/p_arquivo_titulo/`.

## Postman

| Item | Valor |
|------|--------|
| Pasta pai | `Administrativo` |
| Subpasta | `Arquivo Titulo` |
| Variável | `arquivoTituloId` |
| Requests CRUD | All, Create, Get, Update, Delete |
| Requests BLOB | Get Texto, Get Texto Importado |
| Prefix URL | `{{BaseUrlV1}}administrativo/p_arquivo_titulo` |

## Registro `api.py` (proposto)

```python
prefix="/administrativo/p_arquivo_titulo",
tags=["Arquivos de titulo"],
```

Import: `from packages.v1.administrativo.endpoints import p_arquivo_titulo_endpoint` (ou reexport no `endpoints/__init__`).

## Referência de implementação

- CRUD + formato3: `g_feriado`, `p_banco`
- BLOB fora do CRUD: `p_template` (metadados no CRUD; conteúdo em rota separada)
- Model: `model/p_arquivo_titulo.py`

## Escopo explícito fora desta fase

- Show com lista de títulos / resultado Febraban (`P_FEBRABAN_*`)
- PUT/upload nos endpoints de BLOB
- Frontend `PTituloArquivo*` usa API real (`administrativo/p_arquivo_titulo/`); mock removido do DataConfig
