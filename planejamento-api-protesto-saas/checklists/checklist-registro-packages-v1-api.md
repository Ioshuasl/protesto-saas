# Checklist — registro em `packages/v1/api.py`

## Novo módulo de domínio

- [ ] Pasta `api/packages/v1/<modulo>/` com subpastas: actions, controllers, endpoints, repositories, schemas, services
- [ ] `__init__.py` onde necessário
- [ ] Import do endpoint em `api.py`
- [ ] `include_router` com prefix correto (hífen no path HTTP)
- [ ] `tags` descritiva em português

## Módulo existente (`administrativo`)

- [ ] Apenas novo import + bloco `include_router`
- [ ] Ordem alfabética ou agrupamento por domínio (seguir padrão local do arquivo)

## Validação manual

- [ ] `GET <prefix>/` retorna 401 sem token
- [ ] OpenAPI/Swagger lista tag e rotas
- [ ] Path não colide com rota existente (ex.: `t_pessoa` vs `p_pessoa`)

## Snippet de referência

```python
from packages.v1.<modulo>.endpoints import <entidade>_endpoint

api_router.include_router(
    <entidade>_endpoint.router,
    prefix="/<prefixo-dataconfig>",
    tags=["<Tag>"],
)
```
