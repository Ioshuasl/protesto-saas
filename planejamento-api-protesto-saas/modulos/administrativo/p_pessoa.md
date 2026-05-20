# PPessoa

| Campo | Valor |
|-------|-------|
| Prefix | `/administrativo/p_pessoa` |
| DataConfig | `app/src/packages/administrativo/data/PPessoa/ppessoaDataConfig.ts` |
| Fase | 1 |
| Status | planejado (parcial: existe `t_pessoa` em outro prefixo) |

## Atenção

A API legada expõe `t_pessoa` em `/administrativo/t_pessoa`. O frontend protesto consome **`p_pessoa`**. Implementar entidade **`p_pessoa`** separada; não reutilizar rotas `t_pessoa` sem decisão de produto.

## Regras de negócio

- create: validar CPF/CNPJ, tipo de pessoa, campos obrigatórios
- update: conflito documento duplicado (409)
- delete: bloquear com vínculo em título

## Filtros IndexSchema

| Campo | Tipo |
|-------|------|
| nome | str |
| cpfcnpj | str |
| tipo_pessoa | str |

## Arquivos

CRUD `p_pessoa_*` em `administrativo/` (não misturar com `t_pessoa_*`).
