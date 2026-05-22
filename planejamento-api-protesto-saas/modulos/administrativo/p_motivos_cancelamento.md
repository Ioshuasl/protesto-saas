# PMotivosCancelamento

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/p_motivos_cancelamento` |
| DataConfig | `app/src/packages/administrativo/data/PMotivosCancelamento/pmotivosCancelamentoDataConfig.ts` |
| Fase | 1 |
| Status | implementado |

## Regras de negócio

- Motivos para cancelamento/desistência
- create: padronizar classificação e obrigatoriedades
- delete: impedir com uso histórico

## Dependência

- `p_titulo`: `cancelar_titulo`, `desistir_titulo`

## Siglas e filtros

| Coluna | API | Regra |
|--------|-----|-------|
| `SITUACAO` | `A` / `I` | `A` ativo no banco; `I` ou NULL → `I` na resposta |
| `ORD_JUD_OU_REM_IND` | — | Oculto na API (opcional no banco, não exposto) |

**Index:** filtro de negócio apenas `descricao` (LIKE). Formato3: `p`, `per_page`, `sort`.

## Associações ORM

- `P_MOTIVOS_CANCELAMENTO` hasMany `P_TITULO` (`MOTIVO_CANCELAMENTO`)
- `P_TITULO` belongsTo `P_MOTIVOS_CANCELAMENTO`

## Arquivos

CRUD `p_motivos_cancelamento_*` em `administrativo/`. Postman: `Administrativo` / `Motivos Cancelamento`, variável `motivosCancelamentoId`.
