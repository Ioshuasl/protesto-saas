# PCertidao

| Campo | Valor |
|-------|-------|
| Pacote | `packages/v1/administrativo/` |
| Prefix | `/administrativo/p_certidao` |
| DataConfig | `app/src/packages/certidao/data/PCertidao/pCertidaoDataConfig.ts` |
| Fase | 5 |
| Status | em implementação |
| `USE_ORM_FIREBIRD` | `true` |

## Rotas

| Operação | Método | Path |
|----------|--------|------|
| index | GET | `/` |
| show | GET | `/{id}/` |
| create | POST | `/` |
| update | PUT | `/{id}/` |
| delete | DELETE | `/{id}/` |

Fora do escopo desta etapa: `GET /consulta_apresentante/`.

## Descoberta Firebird

Tabela principal: `P_CERTIDAO`.

FKs descobertas:

| Coluna | Tabela destino | Regra nesta etapa |
|--------|----------------|-------------------|
| `USUARIO_ID` | `G_USUARIO.USUARIO_ID` | Campo numérico; sem include |
| `NFSE_ID` | `C_NFSE.NFSE_ID` | Campo numérico; sem include |
| `PROTECAO_CREDITO_ID` | `P_PROTECAO_CREDITO.PROTECAO_CREDITO_ID` | Campo numérico; sem include |

## Siglas

| Coluna | Siglas |
|--------|--------|
| `TIPO_CERTIDAO` | `R` = certidão Serasa; `P` = certidão positiva; `N` = certidão negativa |
| `TIPO_REMESSA` | Quando `TIPO_CERTIDAO = R`: `P` = protesto Serasa; `C` = cancelamento Serasa. Quando `TIPO_CERTIDAO` é `P` ou `N`: `NULL` |
| `STATUS` | `A` = ativo; `C` = cancelado |

## Index formato3

| Item | Valor |
|------|-------|
| PK (fallback sort) | `certidao_id` |
| Campos sort | `certidao_id`, `data_certidao`, `tipo_certidao`, `status`, `cpfcnpj`, `nome` |
| Filtros negócio | `tipo_certidao`, `data_certidao`, `status`, `busca` |
| Paginação resposta | sim — `pagination` no controller |
| Postman All | `?p=1&per_page=20&sort=certidao_id.desc&tipo_certidao=P&status=A` |

## Regras — CRUD

- index: filtros por `tipo_certidao` (`P` ou `N`), `data_certidao`, `status` (`A` ou `C`) e `busca` em `CPFCNPJ` ou `NOME`
- create: gerar `CERTIDAO_ID` via `G_SEQUENCIA` quando não informado
- update: atualização parcial dos campos enviados
- delete: remoção física da certidão e limpeza da sequência gerada

## Regras — consulta_apresentante

Não implementar nesta etapa. Planejado para fase futura.

Query params obrigatórios (validar tipos):

| Param | Tipo |
|-------|------|
| apresentante | str |
| cpfcnpj | str |
| data_inicio | date (opcional com default) |
| data_fim | date (opcional com default) |

Resposta `data` estruturada:

```json
{
  "titulosPorDocumento": [],
  "candidatosHomonimia": []
}
```

- Período padrão operacional: 5 anos quando cliente não informar
- Apenas títulos elegíveis (protesto ativo conforme regra)

## Estrutura

```text
administrativo/
├── endpoints/p_certidao_endpoint.py
├── controllers/p_certidao_controller.py
├── schemas/p_certidao_schema.py
├── services/p_certidao/go/
│   ├── p_certidao_index_service.py
│   ├── p_certidao_show_service.py
│   ├── p_certidao_save_service.py
│   ├── p_certidao_update_service.py
│   └── p_certidao_delete_service.py
└── ...
```

## Models necessários

| Tabela Firebird | Arquivo model | Motivo no escopo |
|-----------------|---------------|------------------|
| `P_CERTIDAO` | `api/packages/v1/administrativo/model/p_certidao.py` | Entidade alvo |

## Registro api.py

```python
prefix="/administrativo/p_certidao",
tags=["Certidões"],
```

## Postman

| Item | Valor |
|------|-------|
| Pasta pai | `Administrativo` |
| Subpasta | `Certidão` |
| Variável | `certidaoId` |
| Requests | All, Create, Get, Update, Delete |
