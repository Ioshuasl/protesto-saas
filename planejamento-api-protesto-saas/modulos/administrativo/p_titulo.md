# PTitulo (fluxo central)

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/p_titulo` |
| DataConfig | `app/src/packages/administrativo/data/PTitulo/ptituloDataConfig.ts` |
| Fase | 2 e 3 |
| Status | planejado |

Documentação detalhada: [03-fluxo-ptitulo.md](../../03-fluxo-ptitulo.md).

## Estrutura de pastas (espelho api)

```text
api/packages/v1/administrativo/
├── endpoints/p_titulo_endpoint.py          # todas as rotas
├── controllers/p_titulo_controller.py    # um método por operação
├── schemas/p_titulo_schema.py              # + schemas por ação quando necessário
├── services/p_titulo/go/
│   ├── p_titulo_index_service.py
│   ├── p_titulo_show_service.py
│   ├── p_titulo_show_devedores_service.py
│   ├── p_titulo_selos_service.py
│   ├── p_titulo_proximo_numero_apontamento_service.py
│   ├── p_titulo_apontar_service.py
│   ├── p_titulo_intimar_service.py
│   ├── p_titulo_aceite_edital_service.py
│   ├── p_titulo_protestar_service.py
│   ├── p_titulo_liquidar_service.py
│   ├── p_titulo_desistir_service.py
│   ├── p_titulo_cancelar_service.py
│   ├── p_titulo_voltar_apontamento_service.py
│   ├── p_titulo_voltar_intimacao_service.py
│   ├── p_titulo_voltar_protesto_service.py
│   ├── p_titulo_update_status_service.py
│   ├── p_titulo_sustar_service.py
│   └── p_titulo_retirada_service.py
├── actions/p_titulo/                       # 1 action por operação de persistência
└── repositories/p_titulo/                # 1 repository por operação SQL
```

## Rotas (resumo)

| Grupo | Rotas |
|-------|-------|
| Leitura | index, show, showDevedores, selos, proximoNumeroApontamento |
| Escrita fluxo | apontar, intimar, aceite_edital, protestar, liquidar, desistir, cancelar, voltar_*, sustar, retirada |
| Manutenção | updateStatus |

## Controller — métodos planejados

`index`, `show`, `showDevedores`, `selos`, `proximoNumeroApontamento`, `apontar`, `intimar`, `aceiteEdital`, `protestar`, `liquidar`, `desistir`, `cancelar`, `voltarApontamento`, `voltarIntimacao`, `voltarProtesto`, `updateStatus`, `sustar`, `retirada`

Cada método de ação retorna:

```python
{"message": "...", "data": <titulo_completo>}
```

## Service transversal

Considerar (somente se reduzir duplicação real):

- `p_titulo_show_service` — recarregar título completo após mutação (reuso interno)
- `p_titulo_state_machine_service` — validar transições (409/422)

Evitar overengineering: preferir validação explícita por service de ação na Fase 3.

## Filtros index (obrigatório)

Alinhar com tipagem frontend — mínimo planejado:

| Campo | Uso |
|-------|-----|
| fase / situacao | apontado, intimacao, protestado |
| ocorrencia_id | triagem |
| data_* | intervalos |
| parte (devedor/apresentante) | busca |
| valor_* | faixa |

## Estimativa de arquivos

- ~20 services de ação + 5 leitura ≈ 25 services
- Mesma quantidade actions + repositories
- **1** endpoint + **1** controller

Implementar em PRs por grupo ([04-ordem-implementacao.md](../../04-ordem-implementacao.md)).

## Testes obrigatórios

- Transição inválida → 409/422
- Ação válida → `data` contém mesmo shape do `show`
- `proximo_numero_apontamento` — concorrência/sequência
