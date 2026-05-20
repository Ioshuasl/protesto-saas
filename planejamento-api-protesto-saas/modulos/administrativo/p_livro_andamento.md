# PLivroAndamento

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/p_livro_andamento` |
| DataConfig | `app/src/packages/administrativo/data/PLivroAndamento/plivroAndamentoDataConfig.ts` |
| Fase | 1 |
| Status | planejado |

## Regras de negócio

- create: validar numeração e disponibilidade
- delete: impedir em uso (protesto/apontamento)

## Arquivos

CRUD `p_livro_andamento_*` em `administrativo/`.
