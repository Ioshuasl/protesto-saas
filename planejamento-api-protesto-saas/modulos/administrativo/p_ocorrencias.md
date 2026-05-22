# POcorrencias

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/p_ocorrencias` |
| DataConfig | `app/src/packages/administrativo/data/POcorrencias/pocorrenciasDataConfig.ts` |
| Fase | 1 |
| Status | implementado |

## Siglas / domínio (`TIPO`)

| API (gravação) | Significado |
|----------------|-------------|
| `CADASTRO` | Cadastro |
| `APONTADO` | Apontado |
| `INTIMACAO` | Intimação |
| `ACEITE` | Aceite |
| `DESISTENCIA` | Desistência |
| `PAGAMENTO` | Pagamento |
| `CANCELAMENTO` | Cancelamento |
| *(vazio/NULL)* | Permitido na leitura e gravação |

Legado no banco (`CANC/PAGTO`, `PROTESTO`, etc.) permanece na resposta; novos registros usam apenas os valores da tabela acima.

## Regras de negócio

- Cadastro de ocorrências/status para andamento do título
- create: código único (`CODIGO` VARCHAR(10))
- update: código único; `tipo` opcional (vazio limpa o campo)
- delete: bloquear se `P_TITULO.OCORRENCIA_ID` referenciar o registro

## Filtros IndexSchema

| Campo | Tipo | Observação |
|-------|------|------------|
| busca | str | LIKE em `DESCRICAO` **ou** `CODIGO` |
| tipo | str | Igualdade exata (valores válidos da tabela acima) |

## Index formato3

| Item | Valor |
|------|--------|
| PK (fallback sort) | `ocorrencias_id` |
| Campos sort | `ocorrencias_id`, `codigo`, `descricao`, `tipo` |
| Paginação resposta | sim |

## Models / associações

| Tabela | Arquivo | Motivo |
|--------|---------|--------|
| `P_OCORRENCIAS` | `model/p_ocorrencias.py` | Entidade alvo |
| `P_TITULO` | `model/p_titulo.py` | FK delete; `hasMany` / `belongsTo` em `model/index.py` |

## Postman

`api/Orius.postman_collection.json` → `Administrativo` / `Ocorrencias` — variável `{{ocorrenciasId}}`.

## Arquivos

CRUD `p_ocorrencias_*` em `administrativo/` (schemas, repositories, actions, services, controller, endpoint).

**Dependência crítica:** usado por todas as transições de `p_titulo`.
