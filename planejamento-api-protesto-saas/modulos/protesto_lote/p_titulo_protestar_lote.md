# PTituloProtestarBatch

| Campo | Valor |
|-------|-------|
| Pacote | `packages/v1/protesto_lote/` (**novo**) |
| Prefix | `/protesto-lote/p_titulo_protestar_lote` |
| DataConfig | `app/src/packages/protesto-lote/data/PTituloProtestarBatch/pTituloProtestarBatchDataConfig.ts` |
| Fase | 4 |
| Status | planejado |

## Rotas

| Operação | Método | Path |
|----------|--------|------|
| index | GET | `/` |

## Regras de negócio

- Validar elegibilidade de cada título
- Consolidado sucesso/erro por lote
- Consistência transacional por lote/arquivo

## Dependência

- Fase 3 (`p_titulo` protestar) estável

## Arquivos

Entidade `p_titulo_protestar_lote` — index only.
