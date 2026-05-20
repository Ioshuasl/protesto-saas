# PEspecie

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/p_especie` |
| DataConfig | `app/src/packages/administrativo/data/PEspecie/pespecieDataConfig.ts` |
| Fase | 1 |
| Status | planejado |

## Regras de negócio

- create: código/sigla únicos (409)
- update: compatibilidade com títulos já cadastrados
- delete: bloquear com dependência

## Filtros IndexSchema

| Campo | Tipo |
|-------|------|
| codigo | str |
| descricao | str |

## Arquivos

CRUD `p_especie_*` em `administrativo/`.
