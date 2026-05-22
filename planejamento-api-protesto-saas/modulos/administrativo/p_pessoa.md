# PPessoa

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/p_pessoa` |
| DataConfig | `app/src/packages/administrativo/data/PPessoa/ppessoaDataConfig.ts` |
| Fase | 1 |
| Status | implementado |

## Regras de negócio

- CRUD cadastro de pessoas (`P_PESSOA`)
- create/update: validar CPF/CNPJ duplicado (quando informado)
- delete: bloquear se existir `P_PESSOA_VINCULO` ou `P_BANCO.PESSOA_ID`
- `micro_empresa`: S = sim; N, NULL ou vazio = não

## Index formato3

| Item | Valor |
|------|--------|
| PK (fallback sort) | pessoa_id |
| Campos sort | pessoa_id, nome, cpfcnpj, cidade, uf, telefone |
| Filtros negócio | `busca` (unificado: nome → cpfcnpj → telefone, concatenado), cidade (exato), uf (exato) |
| Paginação resposta | sim |

## Models ORM

| Tabela | Arquivo | Motivo |
|--------|---------|--------|
| `P_PESSOA` | `model/p_pessoa.py` | Entidade alvo |
| `P_PESSOA_VINCULO` | `model/p_pessoa_vinculo.py` | Regra delete; domínio título |

## Associações (`model/index.py`)

| Origem | Tipo | Destino | FK |
|--------|------|---------|-----|
| `P_PESSOA` | hasMany | `P_PESSOA_VINCULO` | PESSOA_ID |
| `P_PESSOA_VINCULO` | belongsTo | `P_PESSOA` | PESSOA_ID |
| `P_PESSOA_VINCULO` | belongsTo | `P_TITULO` | TITULO_ID |
| `P_TITULO` | hasMany | `P_PESSOA_VINCULO` | TITULO_ID |

## Domínio P_PESSOA_VINCULO (referência)

| Coluna | API |
|--------|-----|
| `TIPO_VINCULO` | APRESENTANTE, CEDENTE, CREDOR, DEVEDOR |
| `GERAR_SELO` | S / N |
| `DEVEDOR_TIPO_ACEITE` | A (Aceite), E (Edital) |
| `DEVEDOR_MICROEMPRESA` | S / N |
| `PRINCIPAL`, `FAVORECIDO` | ocultos (não expostos) |

## Postman

| Item | Valor |
|------|--------|
| Pasta | `Administrativo` / `Pessoa` |
| Variável | `pessoaId` |
| Requests | All, Create, Get, Update, Delete |
