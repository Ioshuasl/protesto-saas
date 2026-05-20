# PTituloArquivo (CRA)

| Campo | Valor |
|-------|-------|
| Prefix | `/cra/p_arquivo_titulo` |
| DataConfig | `app/src/packages/cra/data/PTituloArquivo/pTituloArquivoDataConfig.ts` |
| Fase | 6 |
| Status | planejado |

## Rotas

| Operação | Método | Path |
|----------|--------|------|
| index | GET | `/` |
| show | GET | `/{id}/` |

## Regras de negócio

- index: metadados de lote, origem, status
- show: relação de títulos + resultado de processamento

## Entidade pasta

`p_arquivo_titulo` (nome arquivo DataConfig: `p_arquivo_titulo`, não `p_titulo_arquivo`).

## Arquivos

index + show (+ repositories/actions correspondentes).
