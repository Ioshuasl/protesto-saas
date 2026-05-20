# Guidelines de Desenvolvimento - Pessoas Juridicas (Administrativo)

Estas guidelines padronizam como evoluir o fluxo de Pessoas Juridicas com seguranca, consistencia e previsibilidade, alinhado ao fluxo documentado em `docs/support/fluxo-pessoas-juridicas.md`.

**Escopo**: `src/app/(protected)/(administrativo)/administrativo/pessoas/juridicas/page.tsx` e cadeia de componentes, hooks, services e data.

**Principio geral**: manter o fluxo em camadas. UI -> Hook -> Service -> Data -> API. Evitar logica de rede direto em componentes.

## Estrutura e responsabilidades

- `page.tsx`: apenas composicao e export do componente principal.
- `TPessoaJuridicaIndex`: orquestracao do fluxo. Sem validacao de schema ou regras de API.
- `TPessoaJuridicaForm`: somente UI do formulario e interacao com `react-hook-form`.
- Hooks (`useTPessoaJuridica*Hook`): concentrar chamadas de service, state local e acoplamento com `ResponseContext`.
- Services (`TPessoaJuridica*Service`): chamar Data layer e aplicar `withClientErrorHandler`.
- Data (`TPessoaJuridica*Data`): definicao de endpoints e metodos HTTP.
- `API`: infraestrutura comum (token, headers, url, serializacao).

## Padrao de evolucao do fluxo

1. Defina a necessidade do usuario e qual etapa do fluxo sera afetada (listagem, detalhe, criacao, edicao, exclusao).
2. Ajuste interface/schemas antes de mexer na UI.
3. Ajuste Data e Service (endpoint e metodo) antes de alterar hook.
4. Ajuste o hook (state, fetch, response).
5. Atualize UI e form (campos, mascaras, validacao).
6. Atualize docs em `docs/support`.

## Camada de UI (componentes)

- Mantenha `TPessoaJuridicaIndex` como coordenador do fluxo.
- Evite efeitos colaterais dentro de renderizacao.
- Use `useCallback` para handlers de acoes.
- Padrao de estados do Index:
- `buttonIsLoading`: controla botao salvar.
- `selectedData`: item em edicao/criacao.
- `isFormOpen`: modal do form.
- `itemToDelete`: item em exclusao.
- `isConfirmOpen`: modal de confirmacao.

## Carregamento e empty state

- Problema atual: `if (tPessoaJuridica.length == 0) return <Loading />;`.
- Recomendacao: controlar `isLoading` separado para evitar loading infinito quando a API retorna lista vazia.
- Padrao sugerido:
- `isLoading = true` antes do fetch.
- `isLoading = false` no finally.
- Se `!isLoading && tPessoaJuridica.length == 0`, renderizar tabela vazia com mensagem.

## Formulario e validacao

- Centralize validacao em `TPessoaJuridicaSchema`.
- Adicione novos campos tanto no schema quanto em `useTPessoaJuridicaFormHook` defaults.
- Use mascaras apenas na UI (`FormatCPFCNPJForm`, `FormatCEP`) e persista valores desmascarados.
- Ao carregar dados de edicao, sempre usar `ResetFormIfData`.

## Tabela e colunas

- `filterColumn` deve apontar para um `id` de coluna existente.
- Se usar `accessorFn`, garantir `sortingFn` coerente.
- Acoes devem permanecer em `TPessoaJuridicaColumns` para manter consistencia do dropdown.

## Hooks

- Manter um hook por responsabilidade: index, save, show, delete.
- Sempre usar `setResponse(response)` para garantir feedback global.
- Retornar dados brutos quando o chamador precisa atualizar estado local.

## Services e Data

- Services devem apenas orquestrar Data e tratamento de erros.
- Data deve conter apenas endpoint, metodo e corpo.
- Endpoints usados:
- Listagem: `GET administrativo/t_pessoa/tipo/J`.
- Detalhe: `GET administrativo/t_pessoa/{pessoa_id}`.
- Criacao: `POST administrativo/t_pessoa/`.
- Edicao: `PUT administrativo/t_pessoa/{pessoa_id}`.
- Exclusao: `DELETE administrativo/t_pessoa/{pessoa_id}`.

## API e contrato

- `API.send` filtra campos `null` e `''` do body.
- Validacoes de URL, token e content-type sao feitas em `ApiSchema`.
- Evite enviar campos opcionais vazios quando o backend nao precisa.

## Representantes (subfluxo)

- Representantes so devem aparecer se `pessoa_id` existir.
- Mantenha o fluxo ancorado em `pessoa_id`.
- Se o backend exigir estado recem-criado, forcar salvar antes de habilitar a aba.

## Tratamento de erros

- `withClientErrorHandler` retorna status `600` em erro local.
- UI deve mostrar mensagem de erro via `ResponseContext`.
- Evitar `try/catch` duplicado em componentes.

## Nomenclatura e tipagem

- Interfaces no padrao `TPessoaJuridicaInterface`.
- Props de componentes em `*Interface`.
- Evitar `any`.

## Checklist para novas features

1. Campo novo no backend? Atualize interfaces e schema.
2. Atualize defaults do form.
3. Atualize UI do form com mascaras e labels.
4. Atualize tabela se o campo precisar ser listado.
5. Garanta que `ResponseContext` receba respostas.
6. Atualize docs.

## Checklist para refactors

1. Nao quebrar chain UI -> Hook -> Service -> Data.
2. Nao mover logica de API para componente.
3. Garantir compatibilidade de endpoints.
4. Garantir consistencia de loading e empty state.

## Arquivos de referencia

- `src/app/(protected)/(administrativo)/administrativo/pessoas/juridicas/page.tsx`
- `src/packages/administrativo/components/TPessoa/TPessoaJuridica/TPessoaJuridicaIndex.tsx`
- `src/packages/administrativo/components/TPessoa/TPessoaJuridica/TPessoaJuridicaForm.tsx`
- `src/packages/administrativo/components/TPessoa/TPessoaJuridica/TPessoaJuridicaTable.tsx`
- `src/packages/administrativo/components/TPessoa/TPessoaJuridica/TPessoaJuridicaColumns.tsx`
- `src/packages/administrativo/hooks/TPessoa/TPessoaJuridica/*.ts`
- `src/packages/administrativo/services/TPessoa/TPessoaJuridica/*.ts`
- `src/packages/administrativo/data/TPessoa/TPessoaJuridica/*.ts`
- `src/packages/administrativo/schemas/TPessoa/*.ts`
- `src/shared/services/api/Api.ts`
- `src/shared/components/confirmDialog/*`
