# Módulo `administrativo` — cadastros e título

Pacote existente: `api/packages/v1/administrativo/`.

Novas entidades protesto usam o **mesmo pacote** com prefixos `administrativo/<entidade>` no HTTP.

## Entidades deste domínio

| Arquivo | Entidade | Tipo |
|---------|----------|------|
| [g_feriado.md](./g_feriado.md) | GFeriado | CRUD |
| [p_banco.md](./p_banco.md) | PBanco | CRUD |
| [p_especie.md](./p_especie.md) | PEspecie | CRUD |
| [p_ocorrencias.md](./p_ocorrencias.md) | POcorrencias | CRUD |
| [p_motivos.md](./p_motivos.md) | PMotivos | CRUD |
| [p_motivos_cancelamento.md](./p_motivos_cancelamento.md) | PMotivosCancelamento | CRUD |
| [p_pessoa.md](./p_pessoa.md) | PPessoa | CRUD (novo; ≠ t_pessoa) |
| [p_livro_andamento.md](./p_livro_andamento.md) | PLivroAndamento | CRUD |
| [p_livro_natureza.md](./p_livro_natureza.md) | PLivroNatureza | CRUD |
| [g_usuario.md](./g_usuario.md) | GUsuario | existente — validar |
| [p_titulo.md](./p_titulo.md) | PTitulo | fluxo central |
