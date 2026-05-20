# GFeriado

| Campo | Valor |
|-------|-------|
| Pacote | `packages/v1/administrativo/` |
| Prefix | `/administrativo/g_feriado` |
| DataConfig | `app/src/packages/administrativo/data/GFeriado/gferiadoDataConfig.ts` |
| Tabela | `G_FERIADO` |
| Fase | 1 |
| Status | implementado |

## Rotas

| Operação | Método | Path |
|----------|--------|------|
| index | GET | `/` |
| show | GET | `/{id}/` |
| create | POST | `/` |
| update | PUT | `/{id}/` |
| delete | DELETE | `/{id}/` |

## Siglas (Firebird → API)

Documentado após `describe_table` + amostra de registros (Firebird 4.0.5).

| Coluna | Sigla API | Significado |
|--------|-----------|-------------|
| `TIPO` | `F` | Fixo |
| `TIPO` | `V` | Variável |
| `SITUACAO` | `A` | Ativo |
| `SITUACAO` | `I` | Inativo (`I`, `NULL` ou vazio no banco → `I` na resposta) |

API usa **apenas siglas** em query (`?tipo=F&situacao=A`), body e resposta.

## Regras de negócio

- index: ordenar por `DATA ASC`; filtros `ano`, `tipo`, `situacao`, `descricao`
- create/update: data obrigatória; duplicidade mesma `data` + `tipo` → HTTP 409
- delete: físico (`DELETE` na tabela)

## Arquivos

| Camada | Arquivos |
|--------|----------|
| model | `model/g_feriado.py` |
| schema | `schemas/g_feriado_schema.py` |
| repositories | `g_feriado_index_repository.py`, `_show_`, `_save_`, `_update_`, `_delete_`, `_get_by_data_tipo_` |
| demais | actions, services, controller, endpoint (padrão CRUD) |

Sem arquivos auxiliares em `repositories/g_feriado/`.

## Persistência (`USE_ORM_FIREBIRD` em `api/.env`)

| Valor | Modo |
|-------|------|
| `true` | `orm-firebird-py` + model; index com filtros string usa SQL no repository |
| `false` | SQL explícito via `BaseRepository` |

Debug: `USE_ORM_FIREBIRD=true python3 scripts/describe_g_feriado_schema.py` (pasta `api/`).

## Registro api.py

```python
prefix="/administrativo/g_feriado",
tags=["Feriados"],
```

## Postman

Pasta `Administrativo` → `Feriado`: All, Create, Get, Update, Delete — siglas `F`/`V`, `A`/`I`.
