# Ordem de implementação

Objetivo: entregar valor incremental com dependências respeitadas e contrato estável para o frontend.

## Fase 0 — Preparação (sem código de negócio)

- [ ] Validar tabelas Firebird para cada entidade `p_*` / `g_feriado`
- [ ] Resolver [05-discrepancias-frontend-doc.md](./05-discrepancias-frontend-doc.md) com produto
- [ ] Criar módulos vazios em `packages/v1/`: `certidao`, `cra`, `apontamento_lote`, `intimacao_lote`, `protesto_lote` (pastas + `__init__.py`)
- [ ] Atualizar `docs/rules/rules_backend_crud_tdd.md` quando convenções forem fixadas

## Fase 1 — Cadastros administrativos (CRUD)

Ordem sugerida (menor acoplamento primeiro):

1. `g_feriado` — impacto em cálculo de prazos
2. `p_banco`, `p_especie`
3. `p_ocorrencias`, `p_motivos`, `p_motivos_cancelamento`
4. `p_livro_andamento`, `p_livro_natureza`
5. `p_pessoa` (novo prefixo; não confundir com `t_pessoa` existente)
6. `g_usuario` — revisar compatibilidade (já existe)

Critério de pronto: CRUD + `index` com filtros tipados + testes unitários por service crítico.

## Fase 2 — `p_titulo` leitura

1. `index` (filtros por fase: apontado, intimacao, protestado, etc.)
2. `show`
3. `selos`
4. `proximo_numero_apontamento`
5. `showDevedores` (se usado na UI)

## Fase 3 — `p_titulo` ações de fluxo

Ordem sugerida (happy path depois rollbacks):

1. `apontar_titulo`
2. `intimar_titulo`
3. `aceite_edital`
4. `protestar_titulo`
5. `liquidar_titulo`, `desistir_titulo`, `cancelar_titulo`
6. `voltar_apontamento`, `voltar_intimacao`, `voltar_protesto`
7. `updateStatus`, `sustar_titulo`, `retirada_titulo`

Critério de pronto: cada ação retorna título completo; testes de transição inválida.

## Fase 4 — Lotes

1. `apontamento_lote` — index
2. `intimacao_lote` — index
3. `protesto_lote` — index

Critério: status de lote, itens com motivo de falha, idempotência documentada.

## Fase 5 — Certidão

1. CRUD `p_certidao`
2. `consulta_apresentante` (query: apresentante, cpfcnpj, data_inicio, data_fim)

## Fase 6 — CRA

1. `cra/importacao` POST save
2. `cra/p_arquivo_titulo` index + show
3. `cra/retorno` index

## Fase 7 — Integração e revisão

- [ ] Postman: `Orius.postman_collection.json` (ou coleção protesto)
- [ ] Desligar mocks por flag no ambiente de homologação
- [ ] Revisão com `skill_python_reviewer.md` em `p_titulo` e CRA

## Paralelização segura

| Pode paralelizar | Não paralelizar |
|------------------|-----------------|
| Cadastros independentes (banco, especie, motivos) | `p_titulo` ações antes do CRUD cadastros |
| CRA vs certidao (após fase 3 estável) | Mesmo arquivo `p_titulo_controller.py` entre devs sem coordenação |
| Testes por entidade | Alteração simultânea de `api.py` sem merge plan |

## Entregável por PR sugerido

1 PR = 1 entidade CRUD completa **ou** 1 grupo coeso de ações `p_titulo` (ex.: apenas apontar+intimar).
