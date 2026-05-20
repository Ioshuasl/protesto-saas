# POcorrencias

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/p_ocorrencias` |
| DataConfig | `app/src/packages/administrativo/data/POcorrencias/pocorrenciasDataConfig.ts` |
| Fase | 1 |
| Status | planejado |

## Regras de negócio

- Cadastro de ocorrências/status para andamento do título
- create: código único + classificação
- update: não invalidar histórico de títulos
- delete: bloquear se já usada em título

## Filtros IndexSchema

| Campo | Tipo |
|-------|------|
| codigo | str |
| descricao | str |
| classificacao | str |

## Arquivos

CRUD `p_ocorrencias_*` em `administrativo/`.

**Dependência crítica:** usado por todas as transições de `p_titulo`.
