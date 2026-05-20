# PROMPT DE REFATORACAO - CAMADA `data`

## Objetivo

Refatorar os arquivos de `src/packages/<PACOTE>/data/<MODULO>/` para garantir:

- responsabilidade unica da camada `data` (integracao externa);
- padronizacao de chamadas HTTP com `API.send` + `Methods`;
- tratamento consistente de erro via `withClientErrorHandler`;
- compatibilidade total com `services` e `hooks` existentes;
- suporte ao modo hibrido (API real + fallback/mock), quando aplicavel.

---

## Contexto arquitetural (obrigatorio)

Na arquitetura do projeto:

- `data` **somente integra** com API/mock/adapters;
- `data` **nao aplica regra de negocio** (isso e de `services`);
- `data` retorna payload bruto/normalizado de transporte;
- `services` orquestram e transformam;
- `hooks` consomem `services`.

Fluxo esperado:

`components -> hooks -> services -> data -> API`

---

## Escopo

- Pasta alvo: `<PROJECT_PATH>/src/packages/<PACOTE>/data/<MODULO>/`
- Arquivos tipicos:
  - `<Modulo>IndexData.ts`
  - `<Modulo>ShowData.ts`
  - `<Modulo>SaveData.ts`
  - `<Modulo>DeleteData.ts`
  - `<modulo>DataConfig.ts` (quando houver estrategia de endpoint/flag)
  - `*InMemory.ts` (quando houver fallback local)

---

## Regras obrigatorias de refatoracao

1. **Padrao de transporte HTTP**
   - Usar `API` de `@/shared/services/api/Api`.
   - Usar `Methods` de `@/shared/services/api/enums/ApiMethodEnum`.
   - Nao hardcodar implementacao de fetch/axios fora do padrao do projeto.

2. **Tratamento de erro padronizado**
   - Encapsular chamadas com `withClientErrorHandler`.
   - Manter mensagem/estrutura de erro compativeis com o restante do modulo.

3. **Contrato estavel para camadas superiores**
   - Nao quebrar assinatura publica de funcoes consumidas por `services`.
   - Preservar tipos de retorno esperados (`Interface[]`, `Interface`, `ApiResponseInterface`, etc.).

4. **Separacao de responsabilidade**
   - Nao mover regra de negocio para `data`.
   - Nao fazer transformacoes de dominio complexas em `data`.
   - Apenas validacoes minimas de integridade de payload para decidir fallback.

5. **Estrategia hibrida API/mock (quando existir no modulo)**
   - Respeitar flag/config de mock do modulo.
   - Se API falhar ou retornar payload invalido para o contrato esperado, usar fallback local.
   - Centralizar endpoints, flags e chaves de configuracao em `<modulo>DataConfig.ts`.

6. **Padrao de imports e organizacao**
   - Ordenar imports por contexto (modulo -> shared).
   - Evitar duplicacao de utilitarios ja existentes em `shared`.

---

## Template de implementacao (referencia)

```ts
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

import { MODULO_ENDPOINTS, useModuloMockData } from "./moduloDataConfig";
import { moduloListRef } from "./moduloInMemory";
import type { ModuloInterface } from "@/packages/<PACOTE>/interfaces/<MODULO>/ModuloInterface";

export async function ModuloIndexData(): Promise<ModuloInterface[]> {
  if (!useModuloMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: MODULO_ENDPOINTS.index,
      }),
    );

    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && Array.isArray(response?.data)) {
      return response.data as ModuloInterface[];
    }
  }

  return [...moduloListRef.current];
}
```

> Observacao: o template e uma base. Ajustar assinatura, metodo HTTP, payload e retorno conforme o caso de uso (`Index`, `Show`, `Save`, `Delete`).

---

## Processo sugerido

1. Mapear contratos atuais consumidos por `services` e `hooks`.
2. Refatorar primeiro `*DataConfig` e fallback/mock (se existir).
3. Refatorar `IndexData` e `ShowData` (leitura).
4. Refatorar `SaveData` e `DeleteData` (mutacoes).
5. Conferir compatibilidade com services/hooks sem alterar API publica.
6. Validar lint e consistencia de tipos.

---

## Entregaveis

- Arquivos de `data` do modulo refatorados e padronizados.
- Configuracao de endpoints/mock centralizada e consistente.
- Contratos preservados para `services` e `hooks`.
- Sem erros de lint nos arquivos alterados.

---

## Checklist final

- [ ] Camada `data` sem regra de negocio.
- [ ] `API.send` + `Methods` aplicados corretamente.
- [ ] `withClientErrorHandler` aplicado no padrao do projeto.
- [ ] Fallback API/mock funcionando quando previsto.
- [ ] Contratos de entrada/saida preservados.
- [ ] Imports organizados e sem duplicacao.
- [ ] `ReadLints` sem erros nos arquivos alterados.
