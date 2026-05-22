# POcorrenciaAndamento

| Campo | Valor |
|-------|-------|
| Pacote | `packages/v1/administrativo/` |
| Prefix | `/administrativo/p_ocorrencia_andamento` |
| Tabela | `P_OCORRENCIA_ANDAMENTO` |
| Status | implementado |
| `USE_ORM_FIREBIRD` | `true` |

## Schema Firebird

| Coluna | Tipo | Nullable |
|--------|------|----------|
| `OCORRENCIA_ANDAMENTO_ID` | NUMERIC(10,2) PK | não |
| `CODIGO` | VARCHAR(10) | sim |
| `DESCRICAO` | VARCHAR(260) | sim |

Sem coluna `SITUACAO`.

### FKs

| Filho | Coluna | Pai |
|-------|--------|-----|
| `P_TITULO` | `OCORRENCIA_ANDAMENTO_ID` | `P_OCORRENCIA_ANDAMENTO` |
| `P_ANDAMENTO` | `OCORRENCIA_ANDAMENTO_ID` | `P_OCORRENCIA_ANDAMENTO` |

### Models ORM

| Tabela | Arquivo | Motivo |
|--------|---------|--------|
| `P_OCORRENCIA_ANDAMENTO` | `model/p_ocorrencia_andamento.py` | Entidade alvo |
| `P_TITULO` | `model/p_titulo.py` | Delete/count |
| `P_ANDAMENTO` | `model/p_andamento.py` | Delete/count + associação |

### Associações (`model/index.py`)

| Origem | Tipo | Destino | FK | `as` |
|--------|------|---------|-----|------|
| `P_OCORRENCIA_ANDAMENTO` | `hasMany` | `P_TITULO` | `OCORRENCIA_ANDAMENTO_ID` | `titulos` |
| `P_TITULO` | `belongsTo` | `P_OCORRENCIA_ANDAMENTO` | `OCORRENCIA_ANDAMENTO_ID` | `ocorrencia_andamento` |
| `P_OCORRENCIA_ANDAMENTO` | `hasMany` | `P_ANDAMENTO` | `OCORRENCIA_ANDAMENTO_ID` | `andamentos` |
| `P_ANDAMENTO` | `belongsTo` | `P_OCORRENCIA_ANDAMENTO` | `OCORRENCIA_ANDAMENTO_ID` | `ocorrencia_andamento` |

## Siglas API

| Coluna | Campo API | Regra |
|--------|-----------|-------|
| `CODIGO` | `codigo` | até 10 chars, upper, único |
| `DESCRICAO` | `descricao` | texto livre |

## Index formato3

| Item | Valor |
|------|--------|
| PK (fallback sort) | `ocorrencia_andamento_id` |
| Campos sort | `ocorrencia_andamento_id`, `codigo`, `descricao` |
| Filtros negócio | `descricao` (LIKE) |
| Paginação resposta | sim |

## Postman

| Item | Valor |
|------|--------|
| Pasta | `Administrativo` / `Ocorrencia Andamento` |
| Variável | `ocorrenciaAndamentoId` |
| Requests | All, Create, Get, Update, Delete |
