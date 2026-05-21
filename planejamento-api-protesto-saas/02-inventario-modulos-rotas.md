# Inventário — módulos, rotas e status

Legenda de status:

| Status | Significado |
|--------|-------------|
| `planejado` | Ainda não existe em `api/` |
| `existente` | Já implementado (pode precisar ajuste de contrato) |
| `parcial` | Existe entidade similar com prefixo/nome diferente |

## Matriz consolidada

| # | Módulo frontend | Entidade | Prefixo API (canônico DataConfig) | Operações | Status `api/` | Planejamento |
|---|-----------------|----------|-----------------------------------|-----------|---------------|--------------|
| 1 | administrativo | GFeriado | `/administrativo/g_feriado` | index, show, create, update, delete | planejado | [modulos/administrativo/g_feriado.md](./modulos/administrativo/g_feriado.md) |
| 2 | administrativo | PBanco | `/administrativo/p_banco` | CRUD | planejado | [p_banco.md](./modulos/administrativo/p_banco.md) |
| 3 | administrativo | PEspecie | `/administrativo/p_especie` | CRUD | implementado | [p_especie.md](./modulos/administrativo/p_especie.md) |
| 4 | administrativo | POcorrencias | `/administrativo/p_ocorrencias` | CRUD | planejado | [p_ocorrencias.md](./modulos/administrativo/p_ocorrencias.md) |
| 5 | administrativo | PMotivos | `/administrativo/p_motivos` | CRUD | planejado | [p_motivos.md](./modulos/administrativo/p_motivos.md) |
| 6 | administrativo | PMotivosCancelamento | `/administrativo/p_motivos_cancelamento` | CRUD | planejado | [p_motivos_cancelamento.md](./modulos/administrativo/p_motivos_cancelamento.md) |
| 7 | administrativo | PPessoa | `/administrativo/p_pessoa` | CRUD | parcial (`t_pessoa`) | [p_pessoa.md](./modulos/administrativo/p_pessoa.md) |
| 8 | administrativo | PLivroAndamento | `/administrativo/p_livro_andamento` | CRUD | planejado | [p_livro_andamento.md](./modulos/administrativo/p_livro_andamento.md) |
| 9 | administrativo | PLivroNatureza | `/administrativo/p_livro_natureza` | CRUD | planejado | [p_livro_natureza.md](./modulos/administrativo/p_livro_natureza.md) |
| 10 | administrativo | GUsuario | `/administrativo/g_usuario` | CRUD + auth/me | existente | [g_usuario.md](./modulos/administrativo/g_usuario.md) |
| 11 | administrativo | PTitulo | `/administrativo/p_titulo` | CRUD + 15+ ações | planejado | [p_titulo.md](./modulos/administrativo/p_titulo.md) |
| 12 | apontamento-lote | PTituloApontamentoBatch | `/apontamento-lote/p_titulo_apontamento_lote` | index | planejado | [p_titulo_apontamento_lote.md](./modulos/apontamento_lote/p_titulo_apontamento_lote.md) |
| 13 | intimacao-lote | PTituloIntimacaoBatch | `/intimacao-lote/p_titulo_intimacao_lote` | index | planejado | [p_titulo_intimacao_lote.md](./modulos/intimacao_lote/p_titulo_intimacao_lote.md) |
| 14 | protesto-lote | PTituloProtestarBatch | `/protesto-lote/p_titulo_protestar_lote` | index | planejado | [p_titulo_protestar_lote.md](./modulos/protesto_lote/p_titulo_protestar_lote.md) |
| 15 | certidao | PCertidao | `/certidao/p_certidao` | CRUD + consulta_apresentante | planejado | [p_certidao.md](./modulos/certidao/p_certidao.md) |
| 16 | cra | CraImportacao | `/cra/importacao` | save (POST) | planejado | [cra_importacao.md](./modulos/cra/cra_importacao.md) |
| 17 | cra | PTituloArquivo | `/cra/p_arquivo_titulo` | index, show | planejado | [p_arquivo_titulo.md](./modulos/cra/p_arquivo_titulo.md) |
| 18 | cra | PRetornoCra | `/cra/retorno` | index | planejado | [p_retorno_cra.md](./modulos/cra/p_retorno_cra.md) |

## Contagem de artefatos (estimativa)

| Tipo | CRUD simples (×9) | p_titulo | p_certidao | cra | lotes (×3) | Total aprox. |
|------|-------------------|----------|------------|-----|------------|--------------|
| endpoints | 9 | 1 (+18 rotas) | 1 | 3 | 3 | 17 arquivos |
| controllers | 9 | 1 | 1 | 3 | 3 | 17 |
| schemas | 9 | 1 (+ schemas de ação) | 1 | 3 | 3 | 17+ |
| services | 45 | ~20 | 6 | 5 | 3 | ~79 |
| actions | 45 | ~20 | 6 | 5 | 3 | ~79 |
| repositories | 45 | ~20 | 6 | 5 | 3 | ~79 |

Implementar em fatias por fase ([04-ordem-implementacao.md](./04-ordem-implementacao.md)).

## Mock flags (frontend)

| Entidade | Variável ambiente |
|----------|-------------------|
| PTitulo | `NEXT_PUBLIC_USE_MOCK_PTITULO` |
| GFeriado | `NEXT_PUBLIC_USE_MOCK_GFERIADO` |
| PPessoa | `NEXT_PUBLIC_USE_MOCK_PPESSOA` |
| PCertidao | `NEXT_PUBLIC_USE_MOCK_P_CERTIDAO` |
| CraImportacao | `NEXT_PUBLIC_USE_MOCK_CRAIMPORTACAO` |
| PTituloApontamentoBatch | `NEXT_PUBLIC_USE_MOCK_P_TITULO_APONTAMENTO_BATCH` |
| PTituloIntimacaoBatch | `NEXT_PUBLIC_USE_MOCK_P_TITULO_INTIMACAO_BATCH` |
| PTituloProtestarBatch | `NEXT_PUBLIC_USE_MOCK_P_TITULO_PROTESTAR_BATCH` |
| PTituloArquivo | `NEXT_PUBLIC_USE_MOCK_P_TITULO_ARQUIVO` |
| PRetornoCra | `NEXT_PUBLIC_USE_MOCK_P_RETORNO_CRA` |

Critério de pronto por módulo: com mock flag `false`, hooks/services do app funcionam sem alteração de URL.
