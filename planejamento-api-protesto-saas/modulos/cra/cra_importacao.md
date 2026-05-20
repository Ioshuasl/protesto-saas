# CraImportacao

| Campo | Valor |
|-------|-------|
| Pacote | `packages/v1/cra/` |
| Prefix | `/cra/importacao` |
| DataConfig | `app/src/packages/cra/data/CraImportacao/craImportacaoDataConfig.ts` |
| Fase | 6 |
| Status | planejado |

## Rotas

| Operação | Método | Path |
|----------|--------|------|
| save | POST | `/` |

## Regras de negócio

- Validar schema/formato de entrada
- Enfileirar processamento se volumoso
- Retornar protocolo para rastreio em `data`

## Estrutura sugerida

Opção A (recomendada — alinhada ao path):

```text
cra/
├── endpoints/cra_importacao_endpoint.py
├── controllers/cra_importacao_controller.py
├── schemas/cra_importacao_schema.py
└── services/cra_importacao/go/cra_importacao_save_service.py
```

`DynamicImport`: `set_package("cra").set_table("importacao")` ou tabela real Firebird.

## Registro api.py

```python
prefix="/cra/importacao",
tags=["CRA Importação"],
```
