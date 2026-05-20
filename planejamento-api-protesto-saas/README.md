# Planejamento API — Protesto SaaS

Documentação de planejamento para implementação das rotas do fluxo de edital/intimação/protesto no backend (`api/`), derivada de:

- `app/DATA_CONFIG_ENDPOINTS_FLUXO_EDITAL.md` (regras de negócio e responsabilidades)
- `app/src/packages/**/data/*DataConfig.ts` (rotas canônicas consumidas pelo frontend)
- `api/packages/v1/` (padrão arquitetural existente: Endpoint → Controller → Service → Action → Repository)
- `docs/guidelines/guideline_backend.md`
- `docs/workflows/workflow_backend_crud_package.md`

## Objetivo

Planejar a montagem das rotas em `api/` mantendo:

1. **Mesma estrutura de pastas** do pacote `packages/v1/<modulo>/` (actions, controllers, endpoints, repositories, schemas, services).
2. **Mesmos padrões de nomenclatura** (`*_endpoint.py`, `*_controller.py`, `*_schema.py`, `*_action.py`, `*_repository.py`, `services/<entidade>/go/*_service.py`).
3. **Rotas idênticas** às declaradas nos `DataConfig.ts` (compatibilidade mock → API real).
4. **Contrato de resposta** `{ message, data }` (e `status` quando padronizado no projeto).

## Índice

| Arquivo | Conteúdo |
|---------|----------|
| [00-contrato-base.md](./00-contrato-base.md) | Contrato HTTP, auth, filtros `index`, auditoria, erros |
| [01-espelho-estrutura-api.md](./01-espelho-estrutura-api.md) | Mapa de pastas `api/` e novos módulos `packages/v1/` |
| [02-inventario-modulos-rotas.md](./02-inventario-modulos-rotas.md) | Matriz módulo × rota × status |
| [03-fluxo-ptitulo.md](./03-fluxo-ptitulo.md) | Máquina de estados, ações e regra de retorno completo |
| [04-ordem-implementacao.md](./04-ordem-implementacao.md) | Fases, dependências e critérios de pronto |
| [05-discrepancias-frontend-doc.md](./05-discrepancias-frontend-doc.md) | Divergências doc × DataConfig |
| [agents/](./agents/) | Agentes de planejamento e implementação |
| [modulos/](./modulos/) | Planejamento por entidade |
| [templates/](./templates/) | Templates reutilizáveis |
| [checklists/](./checklists/) | Checklists pré e pós implementação |

## Agentes

- [agent_planejamento_protesto_api.md](./agents/agent_planejamento_protesto_api.md) — coordena planejamento e briefing antes de codar
- [agent_implementacao_modulo_protesto.md](./agents/agent_implementacao_modulo_protesto.md) — executa um módulo/entidade seguindo o workflow CRUD

## Referências obrigatórias na implementação

- `docs/agents/agent_backend.md`
- `docs/guidelines/guideline_backend.md`
- `docs/workflows/workflow_backend_crud_package.md`
- `docs/rules/rules_backend_crud_tdd.md`

## Status geral (2026-05)

Nenhuma entidade do fluxo protesto (`g_feriado`, `p_banco`, `p_titulo`, `p_certidao`, `cra/*`, lotes) foi localizada em `api/packages/v1/` — implementação **planejada**, não iniciada.

Exceção parcial: `g_usuario` e `t_pessoa` existem no módulo `administrativo`, mas com prefixos/entidades diferentes do frontend protesto (`p_pessoa` vs `t_pessoa`).
