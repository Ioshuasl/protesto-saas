# PLivroAndamento

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/p_livro_andamento` |
| DataConfig | `app/src/packages/administrativo/data/PLivroAndamento/plivroAndamentoDataConfig.ts` |
| Fase | 1 (com `p_livro_natureza`) |
| Status | **implementado (API + frontend)** |
| Tabela | `P_LIVRO_ANDAMENTO` |

## Schema Firebird

| Coluna | Tipo | Nullable | Notas |
|--------|------|----------|-------|
| `LIVRO_ANDAMENTO_ID` | NUMERIC(10,-2) | N | PK |
| `LIVRO_NATUREZA_ID` | NUMERIC(10,-2) | Y | FK → `P_LIVRO_NATUREZA` |
| `FOLHA_ATUAL` | NUMERIC(10,-2) | Y | |
| `NUMERO_LIVRO` | NUMERIC(10,-2) | Y | |
| `NUMERO_LIVRO_LETRA` | VARCHAR(3) | Y | Omitido v1 |
| `DATA_ABERTURA` | TIMESTAMP | Y | |
| `DATA_FECHAMENTO` | TIMESTAMP | Y | null = livro aberto |
| `NUMERO_FOLHAS` | NUMERIC(10,-2) | Y | |
| `SIGLA` | VARCHAR(3) | Y | Default = sigla da natureza |
| `USUARIO_ID` | NUMERIC(10,-2) | Y | FK → `G_USUARIO` |

## Regras de negócio

| Regra | Comportamento |
|-------|----------------|
| Livro aberto | `DATA_FECHAMENTO` IS NULL; campo calculado `aberto` no index/show |
| Um aberto por natureza | 409 no create/update se já existir outro aberto para o mesmo `livro_natureza_id` |
| Sigla | Igual à da `P_LIVRO_NATUREZA` vinculada (default da natureza; se informada, deve coincidir) |
| Numeração | `GET .../proximo-numero-livro/{livro_natureza_id}` → `max_numero_livro`, `numero_livro_sugerido` (MAX+1) |
| Delete | 409 se `P_TITULO` referencia `LIVRO_ID_APONTAMENTO` ou `LIVRO_ID_PROTESTO` |
| Index sort padrão | `data_abertura` **DESC** (sem `sort` na query) |
| Filtros index | `busca` (SIGLA LIKE / NUMERO_LIVRO exato), `livro_natureza_id`, `aberto` S/N |

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Lista paginada |
| GET | `/proximo-numero-livro/{livro_natureza_id}` | Sugestão de numeração (antes da rota `/{id}`) |
| GET | `/{livro_andamento_id}` | Show |
| POST | `/` | Create |
| PUT | `/finalizar/{livro_andamento_id}` | Fecha o livro (`data_fechamento` obrigatória; opcional `folha_atual`, `usuario_id`) |
| PUT | `/{livro_andamento_id}` | Update |
| DELETE | `/{livro_andamento_id}` | Delete |

**Finalizar:** 404 se não existir; 409 se já fechado; 422 se `data_fechamento` &lt; `data_abertura`.

Postman: pasta **Administrativo → Livro Andamento**, variável `{{livroAndamentoId}}`.

Script: `api/scripts/describe_p_livro_andamento_schema.py`.

Testes: `api/tests/unit/administrativo/p_livro_andamento/`.

## Diferença `T_LIVRO_ANDAMENTO`

Rotas legado `/administrativo/t_livro_andamento` e tabela `T_LIVRO_ANDAMENTO` permanecem intactas.
