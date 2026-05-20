# PTituloIntimacaoBatch

| Campo | Valor |
|-------|-------|
| Pacote | `packages/v1/intimacao_lote/` (**novo**) |
| Prefix | `/intimacao-lote/p_titulo_intimacao_lote` |
| DataConfig | `app/src/packages/intimacao-lote/data/PTituloIntimacaoBatch/pTituloIntimacaoBatchDataConfig.ts` |
| Fase | 4 |
| Status | planejado |

## Rotas

| Operação | Método | Path |
|----------|--------|------|
| index | GET | `/` |

## Regras de negócio

- Por item: título, etapa, prazo, resultado
- Marcar aptos/não aptos para próxima etapa
- Idempotência em reprocessamento

## Arquivos

Mesmo padrão mínimo do lote de apontamento — entidade `p_titulo_intimacao_lote`.
