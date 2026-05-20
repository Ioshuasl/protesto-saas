# Contrato base — API Protesto SaaS

Fonte: `app/DATA_CONFIG_ENDPOINTS_FLUXO_EDITAL.md` (seções iniciais e regra de compatibilidade).

## Resposta padrão

```json
{
  "status": "success",
  "message": "Mensagem legível",
  "data": {}
}
```

Alinhar com o padrão já usado em controllers existentes (`message` + `data`). Incluir `status` se o frontend/hooks já esperarem (validar por módulo na implementação).

## Autenticação e autorização

- Todos os endpoints protegidos: `Depends(get_current_user)` em `actions.jwt.get_current_user`.
- Autorização por perfil: definir matriz perfil × rota na implementação (fora do escopo deste planejamento; registrar em cada módulo).

## Auditoria

Registrar em operações de escrita e transições de fluxo (`p_titulo`):

- usuário autenticado
- data/hora (timezone do cartório)
- ação (`apontar`, `intimar`, `aceite_edital`, etc.)
- estado anterior e novo (snapshot mínimo ou diff)

## Validação de negócio

- Validar no **Service** antes de persistir.
- Schemas Pydantic validam formato/tipos; regras de domínio ficam no service.
- Erros previsíveis: `400`, `404`, `409`, `422` com mensagem clara.

## Regra obrigatória — endpoints `index`

Todo `GET .../` (listagem) deve:

1. Aceitar filtros via `Depends(get_url_params)` → schema `*IndexSchema`.
2. Validar tipos de cada filtro (rejeitar filtro genérico sem tipo).
3. Manter **nomes de filtros alinhados** aos tipos do frontend (DataConfig / interfaces TS).
4. Suportar composição de filtros + paginação + ordenação quando aplicável.

Padrão de referência em `api/packages/v1/administrativo/endpoints/g_usuario_endpoint.py` (`index` + `GUsuarioIndexSchema`).

## Compatibilidade mock → API real

- Rotas **exatamente** como em `*DataConfig.ts` (ver [05-discrepancias-frontend-doc.md](./05-discrepancias-frontend-doc.md)).
- Semântica de negócio equivalente ao mock.
- Flags `NEXT_PUBLIC_USE_MOCK_*`: troca transparente quando rotas e payload forem compatíveis.

## Registro de rotas

Todo novo endpoint deve ser registrado em `api/packages/v1/api.py`:

```python
api_router.include_router(
    <entidade>_endpoint.router,
    prefix="/<prefixo-do-dataconfig-sem-barra-final>",
    tags=["<Tag legível>"],
)
```

O `prefix` deve coincidir com o path do DataConfig **sem** a barra final do `index` (ex.: DataConfig `administrativo/p_titulo/` → prefix `/administrativo/p_titulo`).
