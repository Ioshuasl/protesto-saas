# PPessoaVinculo

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/p_pessoa_vinculo` |
| DataConfig | _(sem tela dedicada; consumo via API e aninhado em `p_titulo`)_ |
| Fase | 2 |
| Status | implementado |

## Domínio (amostra Firebird)

| Coluna | API | Valores |
|--------|-----|---------|
| `TIPO_VINCULO` | `tipo_vinculo` | APRESENTANTE, CEDENTE, CREDOR, DEVEDOR |
| `GERAR_SELO` | `gerar_selo` | S / N (`''`/NULL → N) |
| `DEVEDOR_MICROEMPRESA` | `devedor_microempresa` | S / N |
| `DEVEDOR_TIPO_ACEITE` | `devedor_tipo_aceite` | A (Aceite), E (Edital) |
| `PRINCIPAL`, `FAVORECIDO` | — | não expostos |

## Models ORM

| Tabela | Arquivo | Status |
|--------|---------|--------|
| `P_PESSOA_VINCULO` | `model/p_pessoa_vinculo.py` | existe |
| Associações | `model/index.py` | pessoa, titulo, estado_civil, profissao |

## Index formato3

| Item | Valor |
|------|--------|
| PK (fallback sort) | pessoa_vinculo_id |
| Campos sort | pessoa_vinculo_id, titulo_id, pessoa_id, nome, cpfcnpj, tipo_vinculo, cidade, uf |
| Filtros negócio | titulo_id, pessoa_id, tipo_vinculo, nome, cpfcnpj, busca |
| Paginação resposta | sim |

## Postman

| Item | Valor |
|------|--------|
| Pasta | `Administrativo` / `Pessoa Vinculo` |
| Variável | `pessoaVinculoId` |
| Requests | All, Create, Get, Update, Delete |

## Regras save/update

- `titulo_id` obrigatório no create; FK validada em `P_TITULO`
- `pessoa_id` opcional; se informado, valida `P_PESSOA`
- PK via `G_SEQUENCIA` / tabela `P_PESSOA_VINCULO`
