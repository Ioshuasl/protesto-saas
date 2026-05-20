# Template — matriz de arquivos por entidade `<entidade>`

Substituir `<entidade>`, `<Entidade>`, `<modulo>`.

## CRUD padrão (5 operações)

| # | Camada | Caminho |
|---|--------|---------|
| 0 | descoberta | `describe_table` + amostra 5–10 rows → documentar em `modulos/**/<entidade>.md` |
| 1 | model (se `USE_ORM_FIREBIRD=true`) | `api/packages/v1/<modulo>/model/<entidade>.py` |
| 2 | schema | `api/packages/v1/<modulo>/schemas/<entidade>_schema.py` (siglas + `normalize_*`) |
| 3 | repository | `api/packages/v1/<modulo>/repositories/<entidade>/<entidade>_index_repository.py` |
| 3 | repository | `.../<entidade>_show_repository.py` |
| 4 | repository | `.../<entidade>_save_repository.py` |
| 5 | repository | `.../<entidade>_update_repository.py` |
| 6 | repository | `.../<entidade>_delete_repository.py` |
| 7 | action | `api/packages/v1/<modulo>/actions/<entidade>/<entidade>_index_action.py` |
| 8 | action | `.../<entidade>_show_action.py` |
| 9 | action | `.../<entidade>_save_action.py` |
| 10 | action | `.../<entidade>_update_action.py` |
| 11 | action | `.../<entidade>_delete_action.py` |
| 12 | service | `api/packages/v1/<modulo>/services/<entidade>/go/<entidade>_index_service.py` |
| 13 | service | `.../<entidade>_show_service.py` |
| 14 | service | `.../<entidade>_save_service.py` |
| 15 | service | `.../<entidade>_update_service.py` |
| 16 | service | `.../<entidade>_delete_service.py` |
| 17 | controller | `api/packages/v1/<modulo>/controllers/<entidade>_controller.py` |
| 18 | endpoint | `api/packages/v1/<modulo>/endpoints/<entidade>_endpoint.py` |
| 19 | registro | `api/packages/v1/api.py` (include_router) |
| 20 | postman | `api/Orius.postman_collection.json` (pasta + requests com siglas) |
| 21 | test | `api/tests/unit/<modulo>/<entidade>/test_<entidade>_index_service.py` (mínimo) |

**Não criar** em `repositories/<entidade>/`: `*_orm_query.py`, `*_sql_query.py`, `*_codec.py`, `*_row_mapper.py`.

## Operação customizada `<operacao>`

Replicar bloco action + service (+ repository) por operação:

| Camada | Caminho |
|--------|---------|
| schema (se payload) | `<entidade>_<operacao>_schema.py` ou campos em UpdateSchema |
| repository | `repositories/<entidade>/<entidade>_<operacao>_repository.py` |
| action | `actions/<entidade>/<entidade>_<operacao>_action.py` |
| service | `services/<entidade>/go/<entidade>_<operacao>_service.py` |
| controller | método `<operacao>()` em `<entidade>_controller.py` |
| endpoint | rota conforme DataConfig |

## Contagem rápida

- CRUD: **~20 arquivos** + testes
- Cada ação extra: **+3 a 4 arquivos** (+ método controller/endpoint)
