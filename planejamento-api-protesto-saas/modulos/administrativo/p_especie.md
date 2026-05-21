# PEspecie

| Campo | Valor |
|-------|-------|
| Pacote | `packages/v1/administrativo/` |
| Prefix | `/administrativo/p_especie` |
| DataConfig | `app/src/packages/administrativo/data/PEspecie/pespecieDataConfig.ts` |
| Tabela | `P_ESPECIE` |
| Fase | 1 |
| Status | implementado |
| `USE_ORM_FIREBIRD` | `true` |

## Rotas — CRUD padrão

| Operação | Método | Path |
|----------|--------|------|
| index | GET | `/` |
| show | GET | `/{especie_id}/` |
| create | POST | `/` |
| update | PUT | `/{especie_id}/` |
| delete | DELETE | `/{especie_id}/` |

## Schema Firebird

| Coluna | Tipo | Nullable |
|--------|------|----------|
| `ESPECIE_ID` | NUMERIC(10,2) PK | não |
| `ESPECIE` | VARCHAR(3) | sim |
| `DESCRICAO` | VARCHAR(260) | sim |

Sem colunas `TIPO`, `SITUACAO` ou similares.

### FKs

| FK | Filho | Pai |
|----|-------|-----|
| (título) | `P_TITULO.ESPECIE_ID` | `P_ESPECIE.ESPECIE_ID` |

### Models ORM

| Tabela | Arquivo | Motivo |
|--------|---------|--------|
| `P_ESPECIE` | `model/p_especie.py` | Entidade alvo |
| `P_TITULO` | `model/p_titulo.py` | Delete/count por `ESPECIE_ID` |

### Associações (`model/index.py`)

| Origem | Tipo | Destino | FK | `as` |
|--------|------|---------|-----|------|
| `P_ESPECIE` | `hasMany` | `P_TITULO` | `ESPECIE_ID` | `titulos` |
| `P_TITULO` | `belongsTo` | `P_ESPECIE` | `ESPECIE_ID` | `especie` |

## Siglas API

| Coluna | Campo API | Regra |
|--------|-----------|-------|
| `ESPECIE` | `especie` | Sigla até 3 caracteres; `strip` + `upper` na entrada e resposta |
| `DESCRICAO` | `descricao` | Texto livre (até 260 no banco) |

## Regras de negócio

- index: filtro `busca` (LIKE em `ESPECIE` ou `DESCRICAO`, OR); formato3 (`p`, `per_page`, `sort`)
- create/update: sigla `especie` única (409, case-insensitive)
- update: **permite** alterar sigla `especie` mesmo com títulos vinculados
- delete físico: 409 se existir `P_TITULO.ESPECIE_ID`
- ID: `GenerateService` / `G_SEQUENCIA` tabela `P_ESPECIE`

## Filtros IndexSchema

| Campo API | Coluna SQL |
|-----------|------------|
| `busca` | `ESPECIE` ou `DESCRICAO` (LIKE OR) |

## Index formato3

| Item | Valor |
|------|--------|
| PK (fallback sort) | `especie_id` |
| Campos sort | `especie_id`, `especie`, `descricao` |
| Filtros negócio | `busca` |
| Paginação resposta | sim |

## Contrato API

```json
{
  "especie_id": 1,
  "especie": "DMI",
  "descricao": "Duplicata Mercantil por Indicação"
}
```

## Arquivos (matriz)

| # | Camada | Arquivo |
|---|--------|---------|
| 1 | model | `model/p_especie.py` |
| 1b | associações | `model/index.py` |
| 2 | schema | `schemas/p_especie_schema.py` |
| 3–7 | repository | `repositories/p_especie/p_especie_{index,show,save,update,delete}_repository.py` |
| 3b | repository | `p_especie_get_by_especie_repository.py` |
| 3c | repository | `repositories/p_titulo/p_titulo_count_by_especie_repository.py` |
| 8–12 | action | `actions/p_especie/p_especie_*_action.py` |
| 13–17 | service | `services/p_especie/go/p_especie_*_service.py` |
| 18 | controller | `controllers/p_especie_controller.py` |
| 19 | endpoint | `endpoints/p_especie_endpoint.py` |
| 20 | registro | `packages/v1/api.py` |
| 21 | postman | `Orius.postman_collection.json` → `Administrativo` / `Especie` (`especieId`) |
| 22 | debug | `scripts/describe_p_especie_schema.py` |

## Postman

- Pasta: `Administrativo` → `Especie`
- Variável: `especieId`
- Requests: All, Create, Get, Update, Delete

## Registro api.py

```python
prefix="/administrativo/p_especie",
tags=["Especies"],
```
