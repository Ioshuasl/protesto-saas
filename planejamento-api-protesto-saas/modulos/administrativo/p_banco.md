# PBanco

| Campo | Valor |
|-------|-------|
| Pacote | `packages/v1/administrativo/` |
| Prefix | `/administrativo/p_banco` |
| DataConfig | `app/src/packages/administrativo/data/PBanco/pbancoDataConfig.ts` |
| Tabela | `P_BANCO` |
| Fase | 1 |
| Status | implementado |
| `USE_ORM_FIREBIRD` | `true` |

## Rotas — CRUD padrão

| Operação | Método | Path |
|----------|--------|------|
| index | GET | `/` |
| show | GET | `/{banco_id}/` |
| create | POST | `/` |
| update | PUT | `/{banco_id}/` |
| delete | DELETE | `/{banco_id}/` |

## Schema Firebird (`describe_table` — Firebird 4.0.5)

| Coluna | Tipo | Tamanho | Nullable |
|--------|------|---------|----------|
| `BANCO_ID` | NUMERIC | PK | não |
| `CODIGO_BANCO` | VARCHAR | 30 | sim |
| `DESCRICAO` | VARCHAR | 60 | sim |
| `PESSOA_ID` | NUMERIC | — | sim |
| `LAYOUT_ID` | NUMERIC | — | sim |
| `APONTAMENTO_PAG_POSTERIOR` | VARCHAR | **1** | sim |
| `CUSTAS_NA_CONFIRMACAO` | VARCHAR | **1** | sim |
| `DEMAIS_DESPESAS` | NUMERIC | — | sim |

### FKs relevantes

| FK | Filho | Pai |
|----|-------|-----|
| `P_BANCO_P_LAYOUT_FK` | `P_BANCO.LAYOUT_ID` | `P_LAYOUT.LAYOUT_ID` |
| `P_BANCO_PESSOA_FK` | `P_BANCO.PESSOA_ID` | `P_PESSOA.PESSOA_ID` |
| `P_TITULO_P_BANCO_FK` | `P_TITULO.BANCO_ID` | `P_BANCO.BANCO_ID` |

**Nota:** `P_BANCO` **não possui** coluna `SITUACAO` (diferente de `G_FERIADO`).

## Amostra (10 registros — `santarita`)

| banco_id | codigo_banco | descricao (resumo) | layout_id | apontamento | custas | pessoa_id |
|----------|--------------|-------------------|-----------|-------------|--------|-----------|
| 300028 | 90R | BARTOFIL… | 25 | S | N | 308322 |
| 300029 | 90F | DETRAN - GO | 25 | S | N | 308004 |
| 300030 | 748 | BANCO SICREDI… | 25 | S | N | 308003 |
| … | … | … | 25 | S | N | … |

`P_LAYOUT` na amostra: `layout_id=25`, `descricao='FEBRABAN 4.3'`.

### Valores distintos (siglas VARCHAR(1))

| Coluna | Valores no banco |
|--------|------------------|
| `APONTAMENTO_PAG_POSTERIOR` | `NULL`, `S` |
| `CUSTAS_NA_CONFIRMACAO` | `N`, `S` |

## Siglas API (confirmado)

| Coluna | Sigla(s) | Significado |
|--------|----------|-------------|
| `APONTAMENTO_PAG_POSTERIOR` | `S`, `N` | `S` = sim; `N` ou `NULL` no banco → `N` na resposta |
| `CUSTAS_NA_CONFIRMACAO` | `S`, `N` | `S` = sim; `N` ou `NULL` no banco → `N` na resposta |

Frontend (`PBancoSimNao`) já usa `S`/`N`.

## Regras de negócio (confirmado)

- **Sem** coluna `SITUACAO` neste CRUD
- index: filtros `descricao`, `codigo` (LIKE em `CODIGO_BANCO`); ordenar por `DESCRICAO ASC`
- create/update: `codigo_banco` único (409); `layout_id` deve existir em `P_LAYOUT` (404 se ausente)
- create/update: **omitir** `pessoa_id` e `demais_despesas` do contrato de escrita; leitura em index/show
- `demais_despesas`: sempre `null` na resposta por enquanto; insert com `NULL` no banco
- delete físico: bloquear 409 se existir `P_TITULO.BANCO_ID`
- ID: `GenerateService` / `G_SEQUENCIA` tabela `P_BANCO`

## Filtros IndexSchema (proposto)

| Campo API | Coluna SQL |
|-----------|------------|
| `descricao` | `DESCRICAO` (LIKE) |
| `codigo` | `CODIGO_BANCO` (LIKE) |

## Contrato API (proposto — espelho frontend)

```json
{
  "banco_id": 300036,
  "codigo_banco": "001",
  "descricao": "BANCO DO BRASIL S/A",
  "layout_id": 25,
  "apontamento_pag_posterior": "S",
  "custas_na_confirmacao": "N",
  "pessoa_id": 308488,
  "demais_despesas": null
}
```

`pessoa_id`: somente leitura (index/show). `demais_despesas`: somente leitura, sempre `null` por enquanto.

## Arquivos (matriz — implementado)

| # | Camada | Arquivo |
|---|--------|---------|
| 1 | model | `model/p_banco.py` |
| 2 | schema | `schemas/p_banco_schema.py` |
| 3–7 | repository | `repositories/p_banco/p_banco_{index,show,save,update,delete}_repository.py` |
| 3b | repository | `p_banco_get_by_codigo`, `p_banco_layout_exists`, `p_banco_count_titulo` |
| 8–12 | action | `actions/p_banco/p_banco_*_action.py` |
| 13–17 | service | `services/p_banco/go/p_banco_*_service.py` |
| 18 | controller | `controllers/p_banco_controller.py` |
| 19 | endpoint | `endpoints/p_banco_endpoint.py` |
| 20 | registro | `packages/v1/api.py` |
| 21 | postman | `Orius.postman_collection.json` → `Administrativo` / `Banco` (variável `bancoId`) |
| 22 | debug | `scripts/describe_p_banco_schema.py` |

Sem `*_orm_query`, `*_codec`, `*_row_mapper`.

## Registro api.py (proposto)

```python
prefix="/administrativo/p_banco",
tags=["Bancos"],
```

## Referência de implementação

- Estrutura: `g_feriado` (repositories explícitos + siglas no schema)
- FK layout: validar `LAYOUT_ID` contra `P_LAYOUT` no save/update
