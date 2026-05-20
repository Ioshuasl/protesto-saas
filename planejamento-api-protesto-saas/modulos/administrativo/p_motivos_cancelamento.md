# PMotivosCancelamento

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/p_motivos_cancelamento` |
| DataConfig | `app/src/packages/administrativo/data/PMotivosCancelamento/pmotivosCancelamentoDataConfig.ts` |
| Fase | 1 |
| Status | planejado |

## Regras de negócio

- Motivos para cancelamento/desistência
- create: padronizar classificação e obrigatoriedades
- delete: impedir com uso histórico

## Dependência

- `p_titulo`: `cancelar_titulo`, `desistir_titulo`

## Arquivos

CRUD `p_motivos_cancelamento_*` em `administrativo/`.
