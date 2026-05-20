# PRetornoCra

| Campo | Valor |
|-------|-------|
| Prefix | `/cra/retorno` |
| DataConfig | `app/src/packages/cra/data/PRetornoCra/pRetornoCraDataConfig.ts` |
| Fase | 6 |
| Status | planejado |

## Rotas

| Operação | Método | Path |
|----------|--------|------|
| index | GET | `/` |

## Regras de negócio

- Mapear retorno externo → status interno
- Separar erro técnico vs erro de negócio na resposta
- Filtros: protocolo, lote, titulo_id

## Filtros IndexSchema

| Campo | Tipo |
|-------|------|
| protocolo | str |
| lote_id | int |
| titulo_id | int |

## Arquivos

`p_retorno_cra_index_*` em pacote `cra/`.

## Registro api.py

```python
prefix="/cra/retorno",
tags=["CRA Retorno"],
```
