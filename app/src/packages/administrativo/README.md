# Pacote `administrativo`

Espelha o padrão do `saas_app`: por entidade, operações **unitárias** em `data/` e `services/` (`Index`, `Show`, `SaveCreate` / `SaveUpdate`, `Delete`), além de `hooks/` e `schemas/`. Guias: `documentacao-markdown/GUIA_ESTRUTURA_MONOLITICA_SAAS_APP_PARA_PROTO.md`, `CONVENCOES_NOMENCLATURA_APP_E_SIDEBAR.md`, `MIGRACAO_PROTOTIPO_PROTESTO_PARA_NEXT.md`.

## Camadas

| Pasta | Responsabilidade |
|-------|------------------|
| `components/` | UI (tabelas, formulários, diálogos) + telas **`PPessoaIndex`**, **`PMotivosIndex`**, … que compõem Read/Save/Delete + filtros/diálogos (espelho de `TCensecIndex.tsx`) |
| `hooks/` | Três ganchos por entidade CRUD (como `TCensec` no `saas_app`): **`use*ReadHook`** (lista = `*IndexService`), **`use*SaveHook`**, **`use*DeleteHook`**. **GUsuario:** só `useGUsuarioReadHook`. **PTitulo:** `usePTituloReadHook` + `usePTituloSaveHook` (`saveTituloStatus`) |
| `services/` | Um arquivo por operação: `PPessoaIndexService`, `PPessoaShowService`, `PPessoaSaveCreateService`, `PPessoaSaveUpdateService`, `PPessoaDeleteService`; fachada `PPessoaService` agrupa para compatibilidade |
| `data/` | Mock em memória + `db.json`; mesmo recorte: `PPessoaIndexData`, `PPessoaShowData`, `PPessoaSaveData` (create/update), `PPessoaDeleteData`; estado mutável em `*InMemory.ts` |
| `interfaces/` | Contratos; barrel `interfaces/index.ts` |
| `schemas/` | Zod por formulário (`PPessoaFormSchema`, `PMotivosFormSchema`, …) |
| `shared/` | Utilitários do pacote (ex.: `mockDbDelay.ts`) |

Fluxo alvo: `components` → `hooks` → `services` → `data` → API.

## Convenção de nomes (como no `saas_app`)

- **Data:** `<Prefixo><Entidade><Ação>Data.ts` — ex.: `PBancoIndexData`, `GFeriadoDeleteData`.
- **Service:** `<Prefixo><Entidade><Ação>Service.ts` — delega ao `Data` homônimo.
- **Hook:** `use<Entidade>ReadHook.ts` / `use<Entidade>SaveHook.ts` / `use<Entidade>DeleteHook.ts` (nomenclatura alinhada a `useTCensecReadHook`, `useTCensecSaveHook`, `useTCensecDeleteHook`).
- **Schema:** `<Entidade>FormSchema.ts` na pasta da entidade em `schemas/`.

**PTitulo:** mutação mock exposta como `PTituloSaveUpdateStatusData` / `PTituloSaveUpdateStatusService` (sem `Delete` no protótipo). **GUsuario:** apenas `Index` (lista para selects).

## Fachadas `*Service.ts`

Arquivos como `PPessoaService.ts` expõem `PessoaService.getAll` → `PPessoaIndexService`, etc., para não quebrar imports legados. Novo código pode importar serviços granulares diretamente.

## Imports

- `@/packages/administrativo/interfaces`
- `@/packages/administrativo/services/<Entidade>/...`
- `@/packages/administrativo/hooks/<Entidade>/...`
- `@/packages/administrativo/schemas/<Entidade>/...`

**Fora do pacote:** `src/components/ui/`, shell `components/protesto/`, `theme-provider`, `mode-toggle`.

Alias: `@/*` → `src/*`.
