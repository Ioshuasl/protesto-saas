# PTemplate

| Campo | Valor |
|-------|-------|
| Pacote | `packages/v1/administrativo/` |
| Prefix | `/administrativo/p_template` |
| Tabela | `P_TEMPLATE` |
| Fase | 1 |
| Status | planejado para CRUD inicial |

## Rotas

| Operacao | Metodo | Path |
|----------|--------|------|
| index | GET | `/` |
| show | GET | `/{id}` |
| create | POST | `/` |
| update | PUT | `/{id}` |
| delete | DELETE | `/{id}` |

## Descoberta Firebird

`USE_ORM_FIREBIRD=true`; schema confirmado por `QueryInterface.describe_table`.

| Coluna | Tipo | Obrigatorio | Contrato inicial API |
|--------|------|-------------|----------------------|
| `TEMPLATE_ID` | `NUMERIC(10,2)` | sim | `template_id` |
| `DESCRICAO` | `VARCHAR(60)` | sim | `descricao` |
| `TEXTO` | `BLOB SUB_TYPE BINARY` | nao | fora do CRUD inicial |

FKs: nenhuma encontrada.

## Amostra

| `TEMPLATE_ID` | `DESCRICAO` | `TEXTO` |
|---------------|-------------|---------|
| `2` | `CERTIDAO POSITIVA` | BLOB RTF compactado (`rtf-zlib`) |
| `1` | `CERTIDAO NEGATIVA` | BLOB RTF compactado (`rtf-zlib`) |

## Siglas

Nao ha colunas `CHAR(1)` / `VARCHAR(1)` no escopo do CRUD inicial.

## Regras de negocio

- index: filtros `template_id`, `descricao`; formato3 com `p`, `per_page`, `sort`.
- sort permitido: `template_id`, `descricao`; fallback `template_id.desc`.
- create/update: manipula apenas `descricao`; `TEXTO` nao entra no body.
- index/show: retorna apenas `template_id` e `descricao`; `TEXTO` nao entra nas consultas.
- create: gera `TEMPLATE_ID` via `G_SEQUENCIA` para tabela `P_TEMPLATE` quando nao informado.
- delete: fisico (`DELETE` na tabela).

## Models necessarios

| Tabela Firebird | Arquivo model | Motivo no escopo |
|-----------------|---------------|------------------|
| `P_TEMPLATE` | `model/p_template.py` | Entidade alvo |

## Associacoes planejadas

Nenhuma associacao planejada nesta fase.

## Arquivos

| Camada | Arquivos |
|--------|----------|
| model | `model/p_template.py` |
| schema | `schemas/p_template_schema.py` |
| repositories | `p_template_index_repository.py`, `_show_`, `_save_`, `_update_`, `_delete_` |
| demais | actions, services, controller, endpoint (padrao CRUD) |

Sem arquivos auxiliares em `repositories/p_template/`.

## Postman

Pasta `Administrativo` -> `Template`: All, Create, Get, Update, Delete.
