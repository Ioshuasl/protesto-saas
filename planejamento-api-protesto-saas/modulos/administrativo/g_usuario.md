# GUsuario

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/g_usuario` |
| DataConfig | `app/src/packages/administrativo/data/GUsuario/gusuarioDataConfig.ts` |
| Fase | 1 (revisão) |
| Status | **existente** em `api/` |

## Já implementado

- `endpoints/g_usuario_endpoint.py`
- `controllers/g_usuario_controller.py`
- services: index, show, save, update, delete, authenticate, me, getEmail, getLogin, getCpf

## Trabalho planejado (não recriar CRUD)

1. Comparar payload mock vs API real (campos de perfil, status)
2. Validar se rotas extras do legado (`/email`, `/login`, `/cpf`) conflitam com protesto
3. Garantir auditoria em alteração de perfil/status (requisito doc)
4. Documentar perfis autorizados por rota `p_titulo`

## Arquivos

Nenhum CRUD novo — apenas ajustes pontuais se gap de contrato for encontrado.
