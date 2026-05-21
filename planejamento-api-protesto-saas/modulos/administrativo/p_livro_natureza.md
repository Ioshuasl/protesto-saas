# PLivroNatureza

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/p_livro_natureza` |
| DataConfig | `app/src/packages/administrativo/data/PLivroNatureza/plivroNaturezaDataConfig.ts` |
| Fase | 1 |
| Status | implementado (API) |
| Tabela | `P_LIVRO_NATUREZA` |

## Schema Firebird (describe_table — santarita)

| Coluna | Tipo | Nullable |
|--------|------|----------|
| `LIVRO_NATUREZA_ID` | NUMERIC(10,-2) | N |
| `NATUREZA_ID` | NUMERIC(10,-2) | Y → FK `G_NATUREZA` |
| `DESCRICAO` | VARCHAR(60) | Y |
| `SITUACAO` | VARCHAR(1) | Y — **A** = Ativo; **I** ou **null** = Inativo |
| `SIGLA` | VARCHAR(3) | Y |
| `TIPO` | VARCHAR(1) | Y |

FK saída: `P_LIVRO_ANDAMENTO.LIVRO_NATUREZA_ID` → `P_LIVRO_NATUREZA.LIVRO_NATUREZA_ID`.

## Amostra real (3 registros — 2026-05)

| ID | SIGLA | DESCRICAO | SITUACAO | TIPO |
|----|-------|-----------|----------|------|
| 1 | AP | APONTAMENTO | null | null |
| 2 | PR | PROTESTO | null | null |
| 3 | AP | APONTAMENTO | null | null |

- `SITUACAO`: só **null** na base → tratar como Inativo na API.
- `TIPO`: só **null** — UI/mock usam `A`/`P`/`PG`; **sigla real** usa `AP`/`PR` (2 chars).
- **Sigla duplicada** (`AP` nos IDs 1 e 3) — definir unicidade na implementação.

## Regras de negócio

- **delete:** 409 se existir qualquer `P_LIVRO_ANDAMENTO` com `LIVRO_NATUREZA_ID` (única regra confirmada).
- `natureza_id`: oculto no contrato de escrita; opcional na leitura.

## Models ORM

- `api/packages/v1/administrativo/model/p_livro_natureza.py`
- `api/packages/v1/administrativo/model/p_livro_andamento.py`
- Associações em `model/index.py` (`hasMany` / `belongsTo`)

## Debug

```bash
cd api && venv/bin/python3 scripts/describe_p_livro_natureza_schema.py --limit 10
```

## Contrato API

| Campo | Escrita | Leitura |
|-------|---------|---------|
| `livro_natureza_id` | auto (G_SEQUENCIA) | sim |
| `sigla` | sim (até 3 chars, duplicata OK) | sim |
| `descricao` | sim | sim |
| `situacao` | `A` ou `I` (`I` → NULL no banco) | `A` ou `I` (NULL → `I`) |
| `tipo` | — | omitido |
| `natureza_id` | — | omitido |

Index: formato3 + `busca` (SIGLA + DESCRICAO).

## Arquivos

CRUD `p_livro_natureza_*` em `administrativo/`; Postman `Administrativo` / `Livro Natureza`; `{{livroNaturezaId}}`.
