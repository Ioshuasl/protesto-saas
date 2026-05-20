# Checklist — CRUD de módulo

## Planejamento

- [ ] Rotas conferidas no `*DataConfig.ts`
- [ ] Arquivo em `planejamento-api-protesto-saas/modulos/` preenchido
- [ ] Briefing aprovado pelo usuário

## Implementação

- [ ] Schemas: base, Id, Save, Update, Index
- [ ] Repositories com SQL parametrizado
- [ ] Actions com `execute()` enxuto
- [ ] Services com regras de negócio e HTTPException
- [ ] Controller com DynamicImport (`set_package`, `set_table`)
- [ ] Endpoint com `get_current_user` e `get_url_params` no index
- [ ] `api.py` com prefix idêntico ao DataConfig

## Qualidade

- [ ] Resposta `{ message, data }`
- [ ] index: filtros tipados, erro claro se inválido
- [ ] Testes unitários dos services críticos
- [ ] Sem SQL/regra de negócio no endpoint
- [ ] `rules_backend_crud_tdd.md` revisado se nova convenção

## Integração frontend

- [ ] Mock desligado (`NEXT_PUBLIC_USE_MOCK_*=false`) testado
- [ ] Hooks/services do app sem alteração de URL
