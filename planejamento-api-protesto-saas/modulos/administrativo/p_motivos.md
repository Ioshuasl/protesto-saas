# PMotivos

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/p_motivos` |
| DataConfig | `app/src/packages/administrativo/data/PMotivos/pmotivosDataConfig.ts` |
| Fase | 1 |
| Status | planejado |

## Regras de negócio

- Motivos de apontamento
- create: validar descricao/codigo
- update: trilha de auditoria
- delete: bloquear em uso

## Arquivos

CRUD `p_motivos_*` em `administrativo/`.
