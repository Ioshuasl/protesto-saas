# Discrepâncias — doc de fluxo × DataConfig (frontend)

**Regra de planejamento:** rotas e paths do **DataConfig** prevalecem sobre `DATA_CONFIG_ENDPOINTS_FLUXO_EDITAL.md` para compatibilidade mock → API.

## Lotes — prefixo e nome da entidade

| Item | `DATA_CONFIG_ENDPOINTS_FLUXO_EDITAL.md` | `*DataConfig.ts` (canônico) |
|------|----------------------------------------|----------------------------|
| Apontamento batch | `GET apontamento-batch/p_titulo_apontamento_batch/` | `GET apontamento-lote/p_titulo_apontamento_lote/` |
| Intimação batch | `GET intimacao-batch/p_titulo_intimacao_batch/` | `GET intimacao-lote/p_titulo_intimacao_lote/` |
| Protesto batch | `GET protesto-batch/p_titulo_protestar_batch/` | `GET protesto-lote/p_titulo_protestar_lote/` |

**Decisão:** implementar prefixos `apontamento-lote`, `intimacao-lote`, `protesto-lote` e nomes `p_titulo_*_lote`.

## PTitulo — rotas extras no DataConfig

Presentes em `ptituloDataConfig.ts`, ausentes no doc de fluxo:

- `GET administrativo/p_titulo/devedores/{id}` (`showDevedores`)
- `PUT administrativo/p_titulo/sustar_titulo/{id}`
- `PUT administrativo/p_titulo/retirada_titulo/{id}`

**Decisão:** incluir no planejamento e implementar conforme regras do mock/UI.

## Pessoa — prefixo

| Frontend protesto | API existente |
|-------------------|---------------|
| `administrativo/p_pessoa/` | `administrativo/t_pessoa/` (outro domínio legado) |

**Decisão:** criar pacote `p_pessoa` separado; não reutilizar rotas `t_pessoa` sem alinhamento explícito de produto.

## Ação a tomar

- [ ] Atualizar `app/DATA_CONFIG_ENDPOINTS_FLUXO_EDITAL.md` para refletir DataConfig (opcional, documentação)
- [ ] Confirmar com time se algum ambiente ainda chama paths `*-batch/*_batch`
