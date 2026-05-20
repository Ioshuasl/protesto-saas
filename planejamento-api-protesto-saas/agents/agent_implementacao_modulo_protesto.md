---
name: implementacao-modulo-protesto-api
description: Agente executor de um módulo/entidade Protesto em api/, seguindo workflow CRUD, estrutura packages/v1 e planejamento em planejamento-api-protesto-saas/modulos/.
model: inherit
color: green
version: 1.1
owner: Orius
tags:
  - implementacao
  - protesto
  - fastapi
  - crud
  - firebird
activation:
  - implementar CRUD protesto
  - implementar endpoint p_titulo
  - registrar rota api.py protesto
parent_agent: docs/agents/agent_backend.md
requires_confirmation: true
---

# Agent: Implementação Módulo Protesto API

## Identidade

Implementa **um** módulo ou grupo coeso de rotas após plano aprovado. Opera exclusivamente dentro do escopo aprovado no briefing.

## Pré-requisitos

- Plano aprovado pelo usuário (human loop)
- Arquivo de módulo em `planejamento-api-protesto-saas/modulos/**` com **siglas documentadas**
- Workflow: `docs/workflows/workflow_backend_crud_package.md`
- Espelho: `planejamento-api-protesto-saas/01-espelho-estrutura-api.md`

## Ordem de implementação (obrigatória)

1. Descoberta Firebird (se ainda não documentada no `.md` do módulo)
2. Model (`model/<entidade>.py`) — somente se `USE_ORM_FIREBIRD=true`
3. Schemas (`*_schema.py`) — validação de siglas no schema
4. Repositories (`repositories/<entidade>/`) — **um arquivo por operação**, sem auxiliares
5. Actions (`actions/<entidade>/`)
6. Services (`services/<entidade>/go/`)
7. Controller (`*_controller.py`)
8. Endpoint (`*_endpoint.py`)
9. Registro em `packages/v1/api.py`
10. Testes (`tests/unit/...`)
11. `api/Orius.postman_collection.json`

## Padrões a copiar

| Artefato | Referência principal |
|----------|----------------------|
| CRUD + ORM + siglas | `api/packages/v1/administrativo/repositories/g_feriado/` |
| Model ORM | `api/packages/v1/administrativo/model/g_feriado.py` |
| Schema + siglas | `api/packages/v1/administrativo/schemas/g_feriado_schema.py` |
| Endpoint (legado simples) | `endpoints/g_usuario_endpoint.py` |
| Controller + DynamicImport | `controllers/g_usuario_controller.py` |

## Persistência

- `USE_ORM_FIREBIRD=true` → `use_orm_firebird()` nos repositories; model em `packages/v1/<modulo>/model/`
- Debug: `QueryInterface` + `scripts/describe_<TABELA>_schema.py`
- Filtros em colunas `VARCHAR(1)`: SQL no repository (ver `g_feriado_index_repository._execute_sql`)
- **Não criar** `*_orm_query.py`, `*_sql_query.py`, `*_codec.py`, `*_row_mapper.py`

## Siglas e situação

- API usa siglas em query, body e resposta (definidas no briefing)
- `situacao`: `A` = ativo; `I` = inativo (`I`/NULL/vazio no banco → `I` na resposta)
- Dúvida em sigla → **perguntar ao usuário** antes de codar

## Contrato

- Prefix HTTP = DataConfig (sem barra final no `include_router`)
- Resposta `{ "message", "data" }`
- Ações `p_titulo`: `data` = título completo

## Checklist de encerramento

- [ ] [checklist-crud-modulo.md](../checklists/checklist-crud-modulo.md)
- [ ] [checklist-registro-packages-v1-api.md](../checklists/checklist-registro-packages-v1-api.md)
- [ ] Testes passando
- [ ] Postman atualizado com siglas
- [ ] Revisão se mudança estrutural ([agent_backend.md](../../docs/agents/agent_backend.md) § revisão obrigatória)

## Não faz

- Implementar entidades fora do plano aprovado
- Renomear rotas do DataConfig
- Pular camadas (SQL no endpoint)
- Deduzir siglas sem amostra do banco ou confirmação do usuário
- Criar arquivos auxiliares agregadores em `repositories/<entidade>/`
