# PTituloApontamentoBatch

| Campo | Valor |
|-------|-------|
| Pacote | `packages/v1/apontamento_lote/` (**novo**) |
| Prefix | `/apontamento-lote/p_titulo_apontamento_lote` |
| DataConfig | `app/src/packages/apontamento-lote/data/PTituloApontamentoBatch/pTituloApontamentoBatchDataConfig.ts` |
| Fase | 4 |
| Status | planejado |

## Rotas

| Operação | Método | Path |
|----------|--------|------|
| index | GET | `/` |

## Regras de negócio

- Status do lote: processando, concluído, erro parcial
- Itens com motivo de falha
- Filtros: período, protocolo, origem
- Idempotência para reprocessamento

## Estrutura mínima

```text
apontamento_lote/
├── endpoints/p_titulo_apontamento_lote_endpoint.py
├── controllers/p_titulo_apontamento_lote_controller.py
├── schemas/p_titulo_apontamento_lote_schema.py
├── services/p_titulo_apontamento_lote/go/p_titulo_apontamento_lote_index_service.py
├── actions/...
└── repositories/...
```

## Registro api.py

```python
prefix="/apontamento-lote/p_titulo_apontamento_lote",
tags=["Lote Apontamento"],
```
