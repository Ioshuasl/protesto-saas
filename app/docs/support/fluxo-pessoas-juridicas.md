# Fluxo - Pessoas Juridicas (Administrativo)

**Arquivo principal**: `src/app/(protected)/(administrativo)/administrativo/pessoas/juridicas/page.tsx`

## Visao geral (cadeia de componentes)

- `page.tsx` exporta `TPessoaJuridicaIndex`.
- `TPessoaJuridicaIndex` organiza:
- `Header` (titulo, descricao, botao "Nova Pessoa").
- `TPessoaJuridicaTable` (listagem e acoes).
- `ConfirmDialog` (exclusao).
- `TPessoaJuridicaForm` (criacao/edicao).

## Fluxo de renderizacao inicial

1. `page.tsx` (client component) renderiza `TPessoaJuridicaIndex`.
2. `TPessoaJuridicaIndex` executa `useEffect` (montagem) e chama `fetchTPessoaJuridica()`.
3. `fetchTPessoaJuridica()` usa `TPessoaJuridicaIndexService` -> `TPessoaJuridicaIndexData` -> `API.send`.
4. Enquanto `tPessoaJuridica.length == 0`, a tela retorna `<Loading type={2} />`.
5. Com dados carregados, a tela exibe header, tabela e modais conforme estados.

## Fluxo de listagem (GET)

- Hook: `useTPessoaJuridicaIndexHook`.
- Service: `TPessoaJuridicaIndexService`.
- Data layer: `TPessoaJuridicaIndexData`.
- Endpoint: `GET administrativo/t_pessoa/tipo/J`.
- Resultado: `response.data` vira `tPessoaJuridica` e a resposta completa e enviada para `ResponseContext` via `setResponse`.

## Fluxo de criacao/edicao (POST/PUT)

1. Usuario clica em "Nova Pessoa".
2. `handleOpenForm(null)` cria `initialData` com `pessoa_tipo: 'J'`.
3. `TPessoaJuridicaForm` abre com `isOpen = true`.
4. Formulario usa `react-hook-form` com `TPessoaJuridicaSchema` (Zod) e defaults de `useTPessoaJuridicaFormHook`.
5. Ao submeter, `handleSave(formData)`:

- `buttonIsLoading = true`.
- Chama `saveTPessoaJuridica(formData)` -> `TPessoaJuridicaSaveService` -> `TPessoaJuridicaSaveData`.
- `TPessoaJuridicaSaveData` decide metodo:
- `POST` se `pessoa_id` inexistente.
- `PUT` se `pessoa_id` existe.
- Endpoint: `administrativo/t_pessoa/${pessoa_id || ''}`.
- Corpo: objeto `formData` filtrado (remove nulos e strings vazias na classe `API`).

6. Depois do save:

- `buttonIsLoading = false`.
- Recarrega lista com `fetchTPessoaJuridica()`.
- Atualiza `selectedData` com o retorno.

## Fluxo de edicao (GET detalhe + PUT)

1. Usuario clica em "Editar" na tabela.
2. `handleOpenForm(item)` define `selectedData` e abre o form.
3. `TPessoaJuridicaForm` chama `executeShowTPessoaJuridica()` se `data.pessoa_id` existe.
4. `fetchTPessoaJuridica(data)` -> `TPessoaJuridicaShowService` -> `TPessoaJuridicaShowData`.
5. Endpoint: `GET administrativo/t_pessoa/{pessoa_id}`.
6. Resposta e aplicada no form via `ResetFormIfData(form, response)`.
7. Ao salvar, segue o mesmo fluxo de save (PUT).

## Fluxo de exclusao (DELETE)

1. Usuario clica em "Remover" na tabela.
2. `handleConfirmDelete(item)` define `itemToDelete` e abre `ConfirmDialog`.
3. Ao confirmar, `handleDelete()` executa:

- `deleteTPessoaJuridica(itemToDelete)` -> `TPessoaJuridicaRemoveService` -> `TPessoaJuridicaRemoveData`.
- Endpoint: `DELETE administrativo/t_pessoa/{pessoa_id}`.
- Recarrega a lista com `fetchTPessoaJuridica()`.
- Fecha modal via `handleCancel()`.

## Tabela (UI e comportamento)

- Componente: `TPessoaJuridicaTable`.
- Base: `DataTable` com `@tanstack/react-table`.
- Colunas definidas em `TPessoaJuridicaColumns`:
- `pessoa_id`.
- `nome_completo` (mostra `nome` e `email`).
- `cpf_cnpj` formatado por `FormatCNPJ`.
- `telefone` formatado por `FormatPhone`.
- `cidade_uf` (concatena `cidade/uf`).
- `data_cadastro` formatado por `FormatDateTime`.
- `actions` com dropdown (editar/remover).
- Filtro configurado: `filterColumn = "nome_completo"`.

## Formulario (UI e campos)

- Componente: `TPessoaJuridicaForm`.
- Modal: `Dialog` (Shadcn UI).
- Tabs:
- `Dados Pessoais` (nome, nome fantasia, inscricoes, CNPJ, observacao).
- `Endereco` (pais, UF, CEP, cidade, municipio, bairro, logradouro, numero, unidade).
- `Representantes` (somente quando `pessoa_id` existe).
- Formatacoes e mascaras:
- `FormatCPFCNPJForm` e `UnmaskCPFCNPJForm` no campo `cpf_cnpj`.
- `FormatCEP` no campo `cep`.

## Representantes (subfluxo dependente do form)

- Renderizado apenas quando existe `data.pessoa_id`.
- Componente: `TPessoaRepresentantePage`.
- Este componente possui fluxo analogo (listagem, save, delete) para representantes vinculados a `pessoa_id`.

## Infraestrutura de API (base comum)

- Classe `API` monta URL absoluta com:
- `NEXT_PUBLIC_ORIUS_APP_API_URL` + `NEXT_PUBLIC_ORIUS_APP_API_PREFIX` + `endpoint`.
- Headers incluem `Authorization: Bearer {token}`.
- `TokenGet()` fornece o token.
- Corpo da requisicao e filtrado para remover `null` e `''`.
- `withClientErrorHandler` envolve services e data com tratamento:
- Em erro, retorna `{ status: 600, message, data }`.

## Estados locais relevantes (TPessoaJuridicaIndex)

- `buttonIsLoading`: loading do botao de salvar.
- `selectedData`: item em edicao/criacao.
- `isFormOpen`: controla modal do formulario.
- `itemToDelete`: item pendente de exclusao.
- `isConfirmOpen`: controla modal de confirmacao.

## Observacoes tecnicas

- Condicao de loading: `if (tPessoaJuridica.length == 0) return <Loading />`. Se a API retornar lista vazia, a tela permanece em loading e a tabela nunca aparece.
- `useTPessoaJuridicaSaveHook` declara `isOpen`, mas esse estado nao e exposto e nao controla o modal.
- `TPessoaJuridicaTable` usa `filterColumn = "nome_completo"` que corresponde a coluna `id: "nome_completo"`, entao o filtro funciona, mas a coluna usa `accessorFn` com o objeto completo e depende do `sortingFn` customizado para ordenacao.

## Arquivos chave

- `src/app/(protected)/(administrativo)/administrativo/pessoas/juridicas/page.tsx`
- `src/packages/administrativo/components/TPessoa/TPessoaJuridica/TPessoaJuridicaIndex.tsx`
- `src/packages/administrativo/components/TPessoa/TPessoaJuridica/TPessoaJuridicaForm.tsx`
- `src/packages/administrativo/components/TPessoa/TPessoaJuridica/TPessoaJuridicaTable.tsx`
- `src/packages/administrativo/components/TPessoa/TPessoaJuridica/TPessoaJuridicaColumns.tsx`
- `src/packages/administrativo/hooks/TPessoa/TPessoaJuridica/useTPessoaJuridicaIndexHook.ts`
- `src/packages/administrativo/hooks/TPessoa/TPessoaJuridica/useTPessoaJuridicaSaveHook.ts`
- `src/packages/administrativo/hooks/TPessoa/TPessoaJuridica/useTPessoaJuridicaDeleteHook.ts`
- `src/packages/administrativo/hooks/TPessoa/TPessoaJuridica/useTPessoaJuridicaShowHook.ts`
- `src/packages/administrativo/data/TPessoa/TPessoaJuridica/*.ts`
- `src/shared/services/api/Api.ts`
- `src/shared/components/confirmDialog/*`
