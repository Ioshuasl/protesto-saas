# PCertidao

| Campo | Valor |
|-------|-------|
| Pacote | `packages/v1/certidao/` (**novo**) |
| Prefix | `/certidao/p_certidao` |
| DataConfig | `app/src/packages/certidao/data/PCertidao/pCertidaoDataConfig.ts` |
| Fase | 5 |
| Status | planejado |

## Rotas

| Operação | Método | Path |
|----------|--------|------|
| index | GET | `/` |
| show | GET | `/{id}/` |
| create | POST | `/` |
| update | PUT | `/{id}/` |
| consultaApresentante | GET | `/consulta_apresentante/` |

## Regras — CRUD

- index: filtros período, tipo, status
- create: elegibilidade do título; identificador único
- update: campos editáveis limitados por regra legal + auditoria

## Regras — consulta_apresentante

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
certidao/
├── endpoints/p_certidao_endpoint.py
├── controllers/p_certidao_controller.py
├── schemas/p_certidao_schema.py
├── services/p_certidao/go/
│   ├── p_certidao_index_service.py
│   ├── p_certidao_show_service.py
│   ├── p_certidao_save_service.py
│   ├── p_certidao_update_service.py
│   └── p_certidao_consulta_apresentante_service.py
└── ...
```

Rota custom no endpoint (antes de `/{id}/` para evitar conflito):

```python
@router.get("/consulta_apresentante/")
```

## Registro api.py

```python
prefix="/certidao/p_certidao",
tags=["Certidão"],
```
