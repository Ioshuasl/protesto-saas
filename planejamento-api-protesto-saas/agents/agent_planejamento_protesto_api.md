---
name: planejamento-protesto-api
description: Agente coordenador do planejamento das rotas Protesto SaaS em api/. Produz briefings, decompõe módulos e valida aderência ao DataConfig e à estrutura packages/v1.
model: inherit
color: blue
version: 1.4
owner: Orius
tags:
  - planejamento
  - protesto
  - fastapi
  - api
  - firebird
  - orm-firebird-py
  - paginacao
  - ordenacao
  - formato3
activation:
  - planejar rotas protesto
  - decompor implementação api
  - revisar aderência DataConfig
  - montar briefing antes de CRUD
parent_agent: docs/agents/agent_backend.md
---

# Agent: Planejamento Protesto API

## Identidade

Coordena o planejamento da API de protesto antes de qualquer código em `api/`. Subordinado às regras de `docs/agents/agent_backend.md` (human loop obrigatório na implementação).

## Escopo

- Ler `planejamento-api-protesto-saas/` e `app/DATA_CONFIG_ENDPOINTS_FLUXO_EDITAL.md`
- Validar rotas contra `app/src/packages/**/data/*DataConfig.ts`
- Produzir briefing no template fixo do agent_backend
- Indicar fase em [04-ordem-implementacao.md](../04-ordem-implementacao.md)
- Apontar arquivos exatos em `api/packages/v1/` (ver [01-espelho-estrutura-api.md](../01-espelho-estrutura-api.md))
- Definir persistência Firebird (ORM vs SQL) e **siglas de domínio** antes da matriz de arquivos
- Exigir **formato3** (`p`, `per_page`, `sort`, `f`) em listagens novas — ver seção Paginação e ordenação

## Não faz

- Implementar Python sem confirmação explícita do usuário
- Alterar rotas do frontend sem decisão registrada em [05-discrepancias-frontend-doc.md](../05-discrepancias-frontend-doc.md)
- Deduzir siglas de colunas `CHAR(1)` / `VARCHAR(1)` sem amostra do banco ou confirmação do usuário

## Fluxo de trabalho

1. Identificar entidade(s) solicitadas no inventário [02-inventario-modulos-rotas.md](../02-inventario-modulos-rotas.md)
2. Abrir planejamento do módulo em `modulos/<dominio>/<entidade>.md`
3. **Inventário de tabelas do prompt** (entidade alvo + toda tabela citada em FK, regra de negócio ou repository — ver seção Models)
4. **Descoberta Firebird** (obrigatória antes de models/repositories — ver seção abaixo)
5. Com `USE_ORM_FIREBIRD=true`: planejar **todos os models** e, em seguida, **todas as associações** em `model/index.py` (nunca o contrário)
6. Preencher matriz de arquivos ([templates/template-matriz-arquivos-por-entidade.md](../templates/template-matriz-arquivos-por-entidade.md))
7. Emitir briefing (Entendimento → Confirmação), incluindo siglas, **grafo de models/FKs** e `USE_ORM_FIREBIRD`
8. **Planejar e documentar** entradas Postman em `api/Orius.postman_collection.json` (ver seção Postman)
9. Após OK, delegar a [agent_implementacao_modulo_protesto.md](./agent_implementacao_modulo_protesto.md) — implementação na ordem: models → `index.py` → schemas → repositories → …

## Carga da documentação ORM (obrigatória com `USE_ORM_FIREBIRD=true`)

Ao planejar ou revisar persistência com ORM, **ler** (ou recarregar no contexto):

1. **[docs/orm-firebird-py/README.md](../../docs/orm-firebird-py/README.md)** — referência completa (`OriusORM`, `define`, `Op`, `QueryInterface`, hooks, charset).
2. **[docs/skills/skill_orm_firebird_py.md](../../docs/skills/skill_orm_firebird_py.md)** — atalho e regras do Protesto SaaS.

Atalho na raiz do monorepo: [orm-firebird-py-readme.md](../../orm-firebird-py-readme.md) (redireciona para o README em `docs/`).

Não implementar repositories ORM sem consultar `describe_table` e a seção de operadores/`Op` quando houver filtros complexos.

Associações (`belongsTo`, `hasOne`, `hasMany`, `belongsToMany`, `include`): seção **“Associações, include…”** em [docs/orm-firebird-py/README.md](../../docs/orm-firebird-py/README.md) (a partir de ~linha 673).

## Models ORM e associações (`model/` + `model/index.py`)

Quando `USE_ORM_FIREBIRD=true`, o prompt do usuário (ou o `.md` do módulo) pode citar **várias tabelas** além da entidade do CRUD. Exemplo: CRUD `P_BANCO` com validação de `P_LAYOUT`, leitura de `PESSOA_ID` → `P_PESSOA`, delete bloqueado se existir `P_TITULO.BANCO_ID` (como em `p_banco_count_titulo_repository.py`).

### 1) Inventário de tabelas (obrigatório no briefing)

Extrair do prompt, do DataConfig, do planejamento e de `list_foreign_keys` / FKs no `.md`:

| Fonte | O que listar |
|-------|----------------|
| Entidade alvo | Tabela principal do CRUD (ex.: `P_BANCO`) |
| Colunas FK no save/show | Tabelas referenciadas (ex.: `P_LAYOUT` via `LAYOUT_ID`) |
| Regras de negócio | Tabelas usadas em validação, contagem ou bloqueio (ex.: `P_TITULO` no delete) |
| Repositories auxiliares planejados | Toda tabela tocada em SQL/ORM (ex.: `LayoutExistsRepository` → `P_LAYOUT`) |
| Includes futuros | Tabelas que entrarão em `include` no ORM |

**Regra:** se o código ou o plano **nomeia a tabela** ou a FK, o **model dessa tabela** entra no inventário — mesmo que ainda não exista CRUD para ela.

Documentar no `.md` do módulo duas tabelas:

**Models necessários**

| Tabela Firebird | Arquivo model | Motivo no escopo |
|-----------------|---------------|------------------|
| `P_BANCO` | `model/p_banco.py` | Entidade alvo |
| `P_LAYOUT` | `model/p_layout.py` | FK `LAYOUT_ID`; validação no save |
| `P_PESSOA` | `model/p_pessoa.py` | Coluna `PESSOA_ID` (leitura index/show) |
| `P_TITULO` | `model/p_titulo.py` | Regra delete: vínculo `BANCO_ID` |

**Associações planejadas** (preencher após models; implementar só em `index.py`)

| Model origem | Tipo | Model destino | `foreignKey` | `as` |
|--------------|------|---------------|--------------|------|
| `P_BANCO` | `belongsTo` | `P_LAYOUT` | `LAYOUT_ID` | `layout` |
| `P_BANCO` | `belongsTo` | `P_PESSOA` | `PESSOA_ID` | `pessoa` |
| `P_BANCO` | `hasMany` | `P_TITULO` | `BANCO_ID` (em `P_TITULO`) | `titulos` |

Confirmar cardinalidade e chaves com `QueryInterface.list_foreign_keys()` e [README associações](../../docs/orm-firebird-py/README.md).

### 2) Ordem de implementação (rigorosa)

| Fase | O que fazer | Proibido nesta fase |
|------|-------------|---------------------|
| **A** | Criar **todos** os arquivos `model/<entidade>.py` do inventário (`*_ATTRIBUTES`, `*_OPTIONS`, `get_*_model()`) | `belongsTo` / `hasMany` em qualquer arquivo individual |
| **B** | Registrar **todas** as associações do módulo em `api/packages/v1/<modulo>/model/index.py` | Schemas, repositories, endpoints |
| **C** | Schemas, repositories, actions, services, controller, endpoint, Postman | — |

- **Um `index.py` por pacote de domínio** (ex.: `administrativo/model/index.py`), importando os `get_*_model()` já definidos e chamando `belongsTo` / `hasOne` / `hasMany` / `belongsToMany` conforme o README.
- Função sugerida: `register_<modulo>_associations()` chamada na inicialização do ORM ou antes do primeiro `findAll` com `include` (definir no briefing quem invoca).
- Models **sem** associação ainda declarada no `index.py` podem existir; associações **nunca** no meio de `p_banco.py` — somente centralizadas no `index.py`.

### 3) `model/index.py` (contrato)

```python
# api/packages/v1/administrativo/model/index.py
from packages.v1.administrativo.model.p_banco import get_p_banco_model
from packages.v1.administrativo.model.p_layout import get_p_layout_model
# ... todos os models do inventário ...

def register_administrativo_associations() -> None:
    P_BANCO = get_p_banco_model()
    P_LAYOUT = get_p_layout_model()
    # P_PESSOA, P_TITULO, ...

    P_BANCO.belongsTo(
        P_LAYOUT,
        {"as": "layout", "foreignKey": "LAYOUT_ID", "targetKey": "LAYOUT_ID"},
    )
    # demais associações do módulo ...
```

- Tipos e nomes de FK: alinhar ao Firebird (`describe_table` + `list_foreign_keys`).
- `as`: camelCase estável para `include` futuro (ex.: `"layout"`, `"titulos"`).
- Repositório que hoje só usa SQL (ex.: `CountTituloRepository`) **ainda exige** model `P_TITULO` no inventário se a tabela está na regra de negócio e `USE_ORM_FIREBIRD=true`.

### 4) Quando o model referenciado ainda não tem CRUD

- Criar mesmo assim `model/<tabela>.py` mínimo (PK + colunas usadas em FK/include/contagem).
- Não atrasar o CRUD da entidade alvo: fase A lista todos os models; implementação pode paralelizar arquivos model, mas **index.py só na fase B**, com **todos** os `get_*_model()` prontos.

### Checklist Models (planejamento)

- [ ] Inventário de tabelas completo a partir do prompt (alvo + referências + regras)
- [ ] `describe_table` / FKs documentados por tabela
- [ ] Matriz lista **cada** `model/<entidade>.py` antes de repositories
- [ ] Tabela de associações prevista (`belongsTo` / `hasMany` / …) com FK e `as`
- [ ] `model/index.py` previsto no pacote `<modulo>` (atualizar se já existir vazio)
- [ ] Implementação delegada com ordem **A → B → C**

## Descoberta Firebird (obrigatória no planejamento)

Antes de listar repositories no briefing:

| Passo | Ação |
|-------|------|
| 1 | Confirmar `USE_ORM_FIREBIRD` em `api/.env` (`true` / `false`) |
| 2 | Com `true`: usar `orm-firebird-py` + `QueryInterface` (`database/orm_firebird.py`, script `api/scripts/describe_<tabela>_schema.py`). **Doc:** [docs/orm-firebird-py/README.md](../../docs/orm-firebird-py/README.md) |
| 2b | `list_foreign_keys()` — mapear grafo para models e `index.py` |
| 3 | `describe_table` — tipos e tamanhos reais (ex.: `VARCHAR(1)`) — **para cada tabela do inventário** |
| 4 | Amostra **5 a 10 registros** da tabela — identificar siglas e valores nulos |
| 5 | Documentar no `.md` do módulo: coluna → sigla API → significado |
| 6 | **Dúvida em sigla ou regra** → perguntar ao usuário; não assumir rótulos do frontend/mock |

Referência implementada: `g_feriado` (`modulos/administrativo/g_feriado.md`).

### Situação (padrão protesto quando aplicável)

| Banco | API (entrada e saída) |
|-------|------------------------|
| `A` | `A` (ativo) |
| `I`, vazio ou `NULL` | `I` (inativo na resposta; filtros aceitam `I`) |

Validação das siglas fica em `*_schema.py`, não em arquivos auxiliares de repository.

## Postman (`api/Orius.postman_collection.json`) — obrigatório

**Toda entidade com rotas novas ou alteradas deve ter pasta na coleção antes de considerar o plano completo.** O agente de planejamento descreve o que será adicionado; o de implementação edita o JSON. Referência: workflow § 6.9 em [workflow_backend_crud_package.md](../../docs/workflows/workflow_backend_crud_package.md).

### Quando atualizar

- Novo CRUD (ex.: `p_banco`)
- Novo endpoint em entidade existente
- Mudança de prefix, query params, body ou siglas de domínio

### Onde inserir

| Item | Regra |
|------|--------|
| Pasta pai | Domínio HTTP do `api.py` (ex.: `Administrativo` para `/administrativo/...`) |
| Subpasta | Nome legível da entidade (ex.: `Banco` para `p_banco`, `Feriado` para `g_feriado`) |
| Ordem sugerida | Após entidade de referência do mesmo domínio ou em ordem alfabética do time |

### Requests obrigatórios (CRUD padrão)

| Nome Postman | Método | URL (exemplo `p_banco`) |
|--------------|--------|-------------------------|
| All | GET | `{{BaseUrlV1}}administrativo/p_banco` + filtros do `IndexSchema` + formato3 (`p`, `per_page`, `sort`) |
| Create | POST | `{{BaseUrlV1}}administrativo/p_banco` |
| Get | GET | `{{BaseUrlV1}}administrativo/p_banco/{{bancoId}}` |
| Update | PUT | `{{BaseUrlV1}}administrativo/p_banco/{{bancoId}}` |
| Delete | DELETE | `{{BaseUrlV1}}administrativo/p_banco/{{bancoId}}` |

### Convenções

- **Auth:** Bearer `{{BearerToken}}` em todas as requests
- **Variável de collection:** `{{<entidade>Id}}` em camelCase (ex.: `bancoId`, `feriadoId`); valor inicial `""` em `variable` da collection
- **Create:** script de teste grava `response.data.<pk>` em `{{bancoId}}` (ex.: `banco_id` → `bancoId`)
- **All / Get / Update / Delete:** scripts de teste padrão (status 200/201 + `message` de sucesso); **não** sobrescrever `{{entidadeId}}` no index
- **Body/query:** usar **siglas** documentadas no `.md` do módulo (`S`/`N`, `F`/`V`, etc.), nunca rótulos longos do mock
- **Descrições** em query params explicando cada sigla
- Após editar: validar JSON (`python3 -c "import json; json.load(open('...'))"`)
- **Index paginado:** incluir `p`, `per_page` e `sort` na request **All** (ver seção Paginação e ordenação)

### Matriz no `.md` do módulo

Incluir bloco Postman na matriz de arquivos:

```markdown
| Postman | `api/Orius.postman_collection.json` → `Administrativo` / `Banco` |
| Variável | `bancoId` |
| Requests | All, Create, Get, Update, Delete |
```

### Exemplo `p_banco` (implementado)

- Prefix: `/administrativo/p_banco`
- Pasta: `Administrativo` → `Banco`
- Query index: `descricao`, `codigo`
- Body create: `codigo_banco`, `descricao`, `layout_id`, `apontamento_pag_posterior`, `custas_na_confirmacao` (`S`/`N`)

## Paginação e ordenação padrão (formato3)

Listagens (`GET` index) do Protesto SaaS usam o **formato3**: query string compartilhada entre frontend e backend para paginação, ordenação e filtros genéricos. Filtros de negócio da entidade (ex.: `ano`, `tipo` em feriado) ficam **separados** e entram no `*IndexSchema`; formato3 entra via `QueryParamsParser`.

### Implementação de referência

| Camada | Arquivo / artefato |
|--------|-------------------|
| Parser HTTP | `api/actions/data/query_params_parser.py` — `QueryParamsParser`, `QueryParams`, `resolve_sort()` |
| Endpoint | `Depends(QueryParamsParser.parse)` + `Depends(get_url_params)` com `_<ENTIDADE>_INDEX_FILTER_KEYS` |
| Repositório ORM/SQL | `query_params.page`, `query_params.per_page`, `QueryParamsParser.resolve_sort(...)` |
| Repositório Pyros | `.paginate(page, per_page)` + `.order_by(campo, direcao)` após `resolve_sort` |
| Frontend | `app/src/shared/actions/api/QueryBuilderAction.ts` — monta `?p=...&per_page=...&sort=...&f=...` |
| Meta UI | `app/src/shared/components/pagination/PaginationMeta.ts` — `page`, `per_page`, `total`, `total_pages` |

**Referências já aderentes:** `g_feriado` (index paginado + sort), `t_pessoa` (`GET /tipo/{pessoa_tipo}` — Pyros + sort), `p_banco` (sort; resposta ainda sem bloco `pagination` — ver exceção abaixo).

### Query string — contrato formato3

| Parâmetro | Obrigatório | Default | Formato | Exemplo |
|-----------|-------------|---------|---------|---------|
| `p` | Não | `1` | inteiro ≥ 1 | `p=2` |
| `per_page` ou `perPage` | Não | `20` | inteiro ≥ 1 | `per_page=50` |
| `sort` | Não | PK **desc** | `campo.asc` ou `campo.desc` | `sort=feriado_id.desc` |
| `f` | Não | — | `campo:operador:valor` (repetível) | `f=cidade:eq:Goiânia` |

- **Body:** index é `GET` — **não** enviar JSON; tudo na query string + Bearer.
- **Aliases:** preferir `per_page` na documentação Postman; o parser aceita `perPage`.

### Ordenação padrão (`sort`)

1. Cliente envia `sort=<campo_logico>.<asc|desc>` (snake_case, alinhado à API).
2. Backend parseia em `QueryParams.sort` (`field`, `direction`).
3. Repositório chama `QueryParamsParser.resolve_sort(query_params, primary_key="<pk>", field_map={...})`:
   - **Com `sort` válido** → usa campo e direção informados.
   - **Sem `sort` / vazio** → **`primary_key` em `desc`** (PK da tabela em ordem decrescente).
   - **Campo desconhecido** (com `field_map`) → fallback **PK desc** (evita SQL injection em `ORDER BY`).

| Stack | Como aplicar |
|-------|----------------|
| **ORM Firebird** (`findAndCountAll`) | `options["order"] = [(COLUNA_DB, "DESC")]` — usar `field_map` snake_case → `COLUNA` Firebird |
| **SQL explícito** | `ORDER BY {coluna} {ASC\|DESC}` — só colunas do `field_map` |
| **Pyros** | `allowed_fields` no `*PyrosRepository`; `.order_by(campo_logico, direcao)` após `resolve_sort` sem `field_map` |

**Planejar no `.md` do módulo:** tabela **Campos de sort permitidos** (nome lógico → coluna Firebird). Exemplo `g_feriado`: `feriado_id`, `data`, `ano`, `descricao`, `tipo`, `situacao`.

### Paginação padrão

1. Endpoint injeta `query_params=Depends(QueryParamsParser.parse)`.
2. Repositório usa `page = query_params.page`, `per_page = query_params.per_page`.
3. **ORM:** `limit` + `offset` com `offset = (page - 1) * per_page`, preferir `findAndCountAll`.
4. **SQL:** `FIRST {per_page} SKIP {offset}` (Firebird).
5. **Pyros:** `.paginate(page, per_page)` na cadeia fluente.
6. Controller de index **paginado** retorna:

```json
{
  "message": "...",
  "data": [ /* linhas da página */ ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

Helper no repositório (padrão `g_feriado_index_repository._build_pagination_meta`):

- `total_pages = ceil(total / per_page)` quando `per_page > 0`.

Frontend: normalizar com `normalizePaginationMeta()` e exibir `Pagination` / `DataTable`.

### Separação: filtros de negócio × formato3

No endpoint index, **não** passar `p`, `per_page`, `sort`, `f` para o `*IndexSchema` (`extra="forbid"` quebra se misturar).

```python
_ENTIDADE_INDEX_FILTER_KEYS = frozenset({"ano", "tipo", ...})  # só filtros do domínio

async def index(
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
):
    filter_data = {k: url_params[k] for k in _ENTIDADE_INDEX_FILTER_KEYS if k in url_params}
    return controller.index(IndexSchema(**filter_data), query_params)
```

| Tipo | Onde | Exemplos |
|------|------|----------|
| Negócio | `*IndexSchema` + `url_params` | `g_feriado`: `ano`, `tipo`, `situacao`, `descricao` |
| Formato3 | `QueryParams` | `p`, `per_page`, `sort`, `f` |

Filtros `f=` (formato3) são para listagens que expõem `allowed_fields` (Pyros) ou evolução futura; hoje `g_feriado` / `p_banco` priorizam filtros no schema.

### Endpoint index — checklist de planejamento

- [ ] `QueryParamsParser.parse` no `GET` de listagem
- [ ] `_<ENTIDADE>_INDEX_FILTER_KEYS` documentado no `.md` e no endpoint
- [ ] `primary_key` e `field_map` de sort no repositório (ou `allowed_fields` Pyros)
- [ ] Fallback documentado: sem `sort` → `<pk>_id desc`
- [ ] Resposta com `pagination` quando a listagem for paginada
- [ ] Postman **All** com `p`, `per_page`, `sort` e descrição dos campos de sort
- [ ] Frontend: `QueryBuilderAction.build()` na camada `*IndexData` quando houver UI paginada

### Postman (index All)

Exemplo mínimo na URL:

```http
GET {{BaseUrlV1}}administrativo/g_feriado?p=1&per_page=20&sort=feriado_id.desc&ano=2026
```

Query params na collection:

| key | value exemplo | description |
|-----|---------------|-------------|
| `p` | `1` | Página (padrão: 1) |
| `per_page` | `20` | Itens por página (padrão: 20) |
| `sort` | `feriado_id.desc` | Opcional. `campo.asc` / `campo.desc`. Sem sort: PK desc |
| … | … | Filtros de negócio da entidade |

### Exceções e migração

| Entidade | Situação | Ação no plano |
|----------|----------|----------------|
| `p_banco` | Sort via formato3; index retorna `data[]` sem `pagination` | Novo CRUD: alinhar a `g_feriado` ou registrar exceção no `.md` |
| `t_pessoa` /tipo | Path `pessoa_tipo` + formato3; Pyros | Documentar PK `pessoa_id` e `allowed_fields` para sort |
| Listagens legadas | Sem `QueryParamsParser` | Planejar migração na matriz de arquivos |

### Matriz no briefing (bloco sugerido)

```markdown
## Index formato3
| Item | Valor |
|------|--------|
| PK (fallback sort) | feriado_id |
| Campos sort | feriado_id, data, ano, mes, dia, descricao, tipo, situacao |
| Filtros negócio | ano, tipo, situacao, descricao |
| Paginação resposta | sim — pagination no controller |
| Postman All | ?p=1&per_page=20&sort=feriado_id.desc&... |
```

## Artefatos obrigatórios no plano

| Artefato | Caminho |
|----------|---------|
| Parser formato3 | `api/actions/data/query_params_parser.py` — usar em todo index novo |
| Models ORM (todos do inventário) | `api/packages/v1/<modulo>/model/<entidade>.py` — **um por tabela referenciada** |
| Associações ORM (após todos os models) | `api/packages/v1/<modulo>/model/index.py` — `register_<modulo>_associations()` |
| Schemas | `api/packages/v1/<modulo>/schemas/<entidade>_schema.py` |
| Repositories (um arquivo por operação) | `api/packages/v1/<modulo>/repositories/<entidade>/` |
| Postman | `api/Orius.postman_collection.json` — **obrigatório** para todo CRUD novo ou alterado (ver seção Postman) |

### Proibido na pasta `repositories/<entidade>/`

- `*_orm_query.py`, `*_sql_query.py`, `*_codec.py`, `*_row_mapper.py` ou agregadores equivalentes
- Cada `*_repository.py` expõe `execute` e métodos privados explícitos (`_execute_orm`, `_execute_sql`, `_map_*_row`, etc.)

## Skills sob demanda

| Skill | Quando |
|-------|--------|
| skill_python.md | Estrutura de pacotes, convenções |
| skill_firebird.md | Modelagem/tabelas, índices, SQL, Firebird 4.x |
| skill_orm_firebird_py.md | API do ORM Python (`orm_py`, `Op`, models, `QueryInterface`) — aponta para [docs/orm-firebird-py/README.md](../../docs/orm-firebird-py/README.md) |
| skill_tdd.md | Estratégia de testes por fase |
| skill_python_reviewer.md | Revisão de plano de `p_titulo` ou CRA |

## Saída esperada do briefing

- Briefing completo (Entendimento → Confirmação)
- Link para arquivo de módulo atualizado com **siglas**, amostra do banco e **tabelas/models/associações**
- **Seção Models:** inventário de tabelas + matriz de arquivos `model/*.py` + tabela de associações para `index.py`
- **Seção Postman:** pasta, variável `{{entidadeId}}`, lista de requests, exemplos de body/query com siglas
- **Seção Index formato3:** PK, campos de `sort`, filtros de negócio, paginação na resposta, exemplo de URL All
- Lista de checks [checklists/](../checklists/) — incluir item Postman atualizado
- Workflow de execução: [docs/workflows/workflow_backend_crud_package.md](../../docs/workflows/workflow_backend_crud_package.md)

### Checklist Postman (planejamento)

- [ ] Pasta da entidade definida em `Orius.postman_collection.json`
- [ ] Cinco requests CRUD (All, Create, Get, Update, Delete) ou justificativa de exceção
- [ ] Variável de collection documentada (`bancoId`, `feriadoId`, …)
- [ ] Bodies e query params com siglas do Firebird, não textos de UI
- [ ] Request **All** com `p`, `per_page`, `sort` (formato3) quando o index for paginado/ordenável
- [ ] Implementação delegada com instrução explícita de editar o Postman ao final

### Checklist Index formato3 (planejamento)

- [ ] `QueryParamsParser` + separação `_INDEX_FILTER_KEYS` previstos no endpoint
- [ ] `resolve_sort` com `primary_key` e `field_map` (ou Pyros `allowed_fields`) no repositório
- [ ] Fallback sem `sort` documentado (PK desc)
- [ ] Contrato de resposta `pagination` definido (ou exceção registrada)
- [ ] Tabela de campos de sort no `.md` do módulo
