# Espelho da estrutura `api/`

Este documento define **onde** cada artefato deve ser criado, replicando o padrão de `api/packages/v1/administrativo/` (referência: `g_usuario`).

## Árvore alvo por entidade (ex.: `p_banco`)

```text
api/
├── packages/v1/
│   ├── api.py                          # registrar include_router
│   └── <modulo_dominio>/               # ver tabela abaixo
│       ├── endpoints/
│       │   └── p_banco_endpoint.py
│       ├── controllers/
│       │   └── p_banco_controller.py
│       ├── model/                        # quando USE_ORM_FIREBIRD=true
│       │   └── p_banco.py
│       ├── schemas/
│       │   └── p_banco_schema.py
│       ├── services/p_banco/go/
│       │   ├── p_banco_index_service.py
│       │   ├── p_banco_show_service.py
│       │   ├── p_banco_save_service.py
│       │   ├── p_banco_update_service.py
│       │   └── p_banco_delete_service.py
│       ├── actions/p_banco/
│       │   ├── p_banco_index_action.py
│       │   ├── p_banco_show_action.py
│       │   ├── p_banco_save_action.py
│       │   ├── p_banco_update_action.py
│       │   └── p_banco_delete_action.py
│       └── repositories/p_banco/
│           ├── p_banco_index_repository.py
│           ├── p_banco_show_repository.py
│           ├── p_banco_save_repository.py
│           ├── p_banco_update_repository.py
│           └── p_banco_delete_repository.py
└── tests/
    ├── unit/<modulo>/<entidade>/...
    └── integration/<modulo>/<entidade>/...   # quando aplicável
```

## Mapeamento: prefixo HTTP → módulo `packages/v1/`

| Prefixo HTTP (DataConfig) | Pacote Python `packages/v1/` | Observação |
|---------------------------|------------------------------|------------|
| `administrativo/*` | `administrativo` | Cadastros + `p_titulo` |
| `certidao/*` | `certidao` | **Novo módulo** |
| `cra/*` | `cra` | **Novo módulo** |
| `apontamento-lote/*` | `apontamento_lote` | **Novo módulo** (nome pasta snake_case) |
| `intimacao-lote/*` | `intimacao_lote` | **Novo módulo** |
| `protesto-lote/*` | `protesto_lote` | **Novo módulo** |

Regra: o **prefix** em `api.py` usa hífen como no frontend (`apontamento-lote`); a **pasta** do pacote usa underscore (`apontamento_lote`), seguindo convenção Python.

## Padrões obrigatórios (copiar de `g_usuario`)

### Endpoint (`*_endpoint.py`)

- `APIRouter()` sem prefix interno (prefix só em `api.py`).
- `Depends(get_current_user)` nas rotas protegidas.
- `Depends(get_url_params)` no `index`.
- Instanciar controller uma vez no módulo.
- Rotas: `GET /`, `GET /{id}`, `POST /`, `PUT /{id}`, `DELETE /{id}` (+ rotas customizadas).

### Controller (`*_controller.py`)

- `DynamicImport().set_package("<modulo>").set_table("<entidade>")` quando seguir padrão administrativo existente.
- Métodos: `index`, `show`, `save`, `update`, `delete` (+ custom).
- Retorno: `{"message": "...", "data": ...}`.

### Service (`services/<entidade>/go/*_service.py`)

- Classe `IndexService`, `ShowService`, `SaveService`, etc.
- Método `execute(self, data: Schema)`.
- Regras de negócio e `HTTPException`.

### Action / Repository

- Action chama repository; persistência no repository via `BaseRepository` e/ou `orm-firebird-py`.
- **Um arquivo por operação** (`*_index_repository.py`, `*_show_repository.py`, …).
- Método público: `execute(...)`. Métodos privados explícitos por responsabilidade (`_execute_orm`, `_execute_sql`, `_map_<entidade>_row`, …).
- **Proibido** na pasta `repositories/<entidade>/`: `*_orm_query.py`, `*_sql_query.py`, `*_codec.py`, `*_row_mapper.py`.

### Persistência Firebird (`USE_ORM_FIREBIRD` em `api/.env`)

| `.env` | Comportamento |
|--------|----------------|
| `USE_ORM_FIREBIRD=true` | Repositórios usam `get_g_<entidade>_model()` de `packages/v1/<modulo>/model/<entidade>.py` quando a operação permitir ORM |
| `USE_ORM_FIREBIRD=false` | SQL explícito via `BaseRepository` em todos os repositories |

Regras:

- Flag lida por `database/orm_firebird_settings.use_orm_firebird()`.
- Conexão ORM: `database/orm_firebird.py` (`get_orm()`, `get_query_interface()`).
- **Debug de schema/tabela:** `QueryInterface.describe_table`, `table_exists`, script `api/scripts/describe_<TABELA>_schema.py` (ex.: `describe_g_feriado_schema.py`).
- Atributos do model devem refletir tamanhos reais do Firebird (ex.: `VARCHAR(1)` → `STRING(2)` no ORM quando o dialect exige; validar com describe).
- Filtros `WHERE` em colunas `VARCHAR` curtas: preferir SQL explícito no repository (limitação conhecida do dialect `sqlalchemy-firebird` com binds).

### Descoberta antes dos repositories (obrigatório)

1. `describe_table` na tabela alvo (Firebird 4.x).
2. SELECT de **5 a 10 registros** — mapear siglas (`TIPO`, `SITUACAO`, etc.).
3. Registrar no planejamento do módulo (`modulos/**/<entidade>.md`).
4. **Dúvida** → perguntar ao usuário; não mapear rótulos do frontend/mock para o banco sem confirmação.

Referência: `g_feriado` — `TIPO`: `F` fixo, `V` variável; `SITUACAO`: `A` ativo, `I`/vazio/`NULL` inativo.

### Model (`model/<entidade>.py`)

- `G_<ENTIDADE>_ATTRIBUTES`, `G_<ENTIDADE>_OPTIONS`, `get_g_<entidade>_model()` com `@lru_cache`.
- Comentário no arquivo documentando domínio Firebird e siglas expostas na API.
- Somente quando `USE_ORM_FIREBIRD=true`.

### Schemas (`*_schema.py`)

- `<Entidade>Schema`, `<Entidade>IdSchema`, `<Entidade>SaveSchema`, `<Entidade>UpdateSchema`, `<Entidade>IndexSchema`.
- Campos de filtro do `index` espelhando tipos do frontend/DataConfig.
- **Validação e normalização de siglas** (`normalize_tipo`, `normalize_situacao`, etc.) ficam no schema — não em codec separado.
- API usa **siglas** em query, body e resposta (ex.: `tipo=F`, `situacao=A`), salvo decisão explícita contrária no briefing.

### Situação (padrão quando coluna é `CHAR(1)` / `VARCHAR(1)`)

| Significado | Banco | API |
|-------------|-------|-----|
| Ativo | `A` | `A` |
| Inativo | `I`, `NULL` ou vazio | `I` na resposta; filtros `situacao=I` devem considerar os três no SQL |

### Postman (`api/Orius.postman_collection.json`)

- Pasta sob domínio HTTP (ex.: `Administrativo` → `<Entidade>`).
- Requests: All (GET index), Create (POST), Get, Update, Delete.
- Query/body com **siglas** alinhadas ao schema.
- Variável de collection para ID após Create (ex.: `feriadoId`).
- Auth: `Bearer {{BearerToken}}`.

## Entidades com operações além do CRUD

Planejar arquivos adicionais na mesma árvore:

| Entidade | Operações extras | Camada principal |
|----------|------------------|------------------|
| `p_titulo` | apontar, intimar, aceite_edital, protestar, liquidar, cancelar, desistir, voltar_*, selos, proximo_numero_apontamento, updateStatus, showDevedores, sustar, retirada | endpoint + controller + service (+ action/repo) **por ação** |
| `p_certidao` | `consulta_apresentante` | endpoint GET dedicado + service |
| `cra/importacao` | `save` (POST) | subpasta `importacao` ou entidade `cra_importacao` |
| Lotes | apenas `index` (por ora) | index_service + index_repository |

## `api.py` — blocos a adicionar (planejado)

```text
# administrativo — protesto cadastros
/administrativo/g_feriado
/administrativo/p_banco
/administrativo/p_especie
/administrativo/p_ocorrencias
/administrativo/p_motivos
/administrativo/p_motivos_cancelamento
/administrativo/p_pessoa
/administrativo/p_livro_andamento
/administrativo/p_livro_natureza
/administrativo/p_titulo

# lotes
/apontamento-lote/p_titulo_apontamento_lote
/intimacao-lote/p_titulo_intimacao_lote
/protesto-lote/p_titulo_protestar_lote

# certidao
/certidao/p_certidao

# cra
/cra/importacao
/cra/p_arquivo_titulo
/cra/retorno
```

`g_usuario`: já registrado em `/administrativo/g_usuario` — validar compatibilidade com `GUsuario` do frontend protesto antes de reutilizar.
