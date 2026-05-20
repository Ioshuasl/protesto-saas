# Regras Executaveis para MCP de Geracao

## Objetivo

Definir uma especificacao executavel para um agente/MCP que gere modulos no padrao do projeto a partir de:

- modulo e entidade;
- endpoints e metodos;
- interfaces e schema zod;
- estrategia de rota `src/app` <-> `src/packages`.

Este documento foi montado a partir dos padroes reais observados em `src/packages` e `src/app`.

---

## 1) Schema de entrada do agente (executavel)

## 1.1 Contrato JSON (v1)

```json
{
  "projectRoot": "src",
  "packageName": "administrativo",
  "domainName": "GFeriado",
  "entityName": "GFeriado",
  "entityNamePlural": "feriados",
  "route": {
    "group": "(protected)",
    "path": "cadastro/feriado",
    "pageKind": "index",
    "componentExportMode": "default"
  },
  "folders": {
    "serviceDirName": "services",
    "interfaceDirName": "interfaces"
  },
  "actions": [
    {
      "name": "index",
      "enabled": true,
      "httpMethod": "GET",
      "endpointKey": "index",
      "responseShape": "array"
    },
    {
      "name": "show",
      "enabled": true,
      "httpMethod": "GET",
      "endpointKey": "show",
      "responseShape": "object",
      "pathParams": ["id"]
    },
    {
      "name": "save",
      "enabled": true,
      "mode": "create_update",
      "create": { "httpMethod": "POST", "endpointKey": "create" },
      "update": { "httpMethod": "PUT", "endpointKey": "update", "pathParams": ["id"] }
    },
    {
      "name": "delete",
      "enabled": true,
      "httpMethod": "DELETE",
      "endpointKey": "delete",
      "pathParams": ["id"]
    }
  ],
  "dataStrategy": {
    "useMockToggle": true,
    "mockToggleEnv": "NEXT_PUBLIC_USE_MOCK_G_FERIADO",
    "hasInMemoryFallback": true,
    "inMemoryRefName": "gferiadoListRef",
    "delayMs": 500
  },
  "contract": {
    "interfaceFile": "GFeriadoInterface.ts",
    "schemaFile": "GFeriadoFormSchema.ts",
    "schemaConstName": "feriadoFormSchema",
    "schemaValuesTypeName": "FeriadoFormValues",
    "idField": "feriado_id"
  },
  "ui": {
    "indexComponentName": "GFeriadoIndex",
    "formComponentName": "FeriadoDialog",
    "tableComponentName": "FeriadoTable",
    "filterComponentName": "FeriadoFilter",
    "pageTitle": "Feriados",
    "createButtonLabel": "Novo Feriado"
  }
}
```

## 1.2 Campos obrigatorios

- `packageName`, `domainName`, `entityName`
- `route.path`, `route.pageKind`
- `folders.serviceDirName`, `folders.interfaceDirName`
- `actions[]` (ao menos `index` ou `save`)
- `contract.idField`

## 1.3 Regras executaveis do schema

1. `folders.serviceDirName` deve ser `service` ou `services`.
2. `folders.interfaceDirName` deve ser `interface` ou `interfaces`.
3. Se `actions.save.mode = create_update`, gerar `SaveCreate` e `SaveUpdate`.
4. Se `dataStrategy.hasInMemoryFallback = true`, exigir `*DataConfig.ts` e `*InMemory.ts`.
5. Se `route.pageKind = index`, componente alvo deve terminar com `Index`.
6. Se `route.pageKind = form`, componente alvo deve terminar com `Form`.

---

## 2) Templates por acao com placeholders

Observacao: placeholders entre `<...>`.

## 2.1 Data - Index

```ts
import { <LIST_REF> } from "@/packages/<PACKAGE>/data/<DOMAIN>/<inMemoryFile>";
import { <ENDPOINTS_CONST>, <USE_MOCK_FN> } from "@/packages/<PACKAGE>/data/<DOMAIN>/<dataConfigFile>";
import type { <ENTITY_INTERFACE> } from "@/packages/<PACKAGE>/<INTERFACE_DIR>/<DOMAIN>/<ENTITY_INTERFACE_FILE>";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function <DOMAIN>IndexData(): Promise<<ENTITY_INTERFACE>[]> {
  if (!<USE_MOCK_FN>()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: <ENDPOINTS_CONST>.index,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && Array.isArray(response?.data)) {
      return response.data as <ENTITY_INTERFACE>[];
    }
  }

  return [...<LIST_REF>.current];
}
```

## 2.2 Data - Show

```ts
export async function <DOMAIN>ShowData(id: number): Promise<<ENTITY_INTERFACE> | null> {
  // mesma estrategia de API + fallback
  // endpoint: <ENDPOINTS_CONST>.show(id)
}
```

## 2.3 Data - Save (create/update)

```ts
export async function <DOMAIN>SaveCreateData(
  data: Omit<<ENTITY_INTERFACE>, "<ID_FIELD>">,
): Promise<<ENTITY_INTERFACE>> {
  // POST + fallback mock
}

export async function <DOMAIN>SaveUpdateData(
  id: number,
  data: Partial<<ENTITY_INTERFACE>>,
): Promise<<ENTITY_INTERFACE>> {
  // PUT + fallback mock
}
```

## 2.4 Data - Delete

```ts
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function execute<DOMAIN>DeleteData(data: <ENTITY_INTERFACE>) {
  // DELETE + fallback mock
}

export const <DOMAIN>DeleteData = withClientErrorHandler(execute<DOMAIN>DeleteData);
```

## 2.5 Service - Pass-through padrao

```ts
"use server";

import { <DOMAIN><ACTION>Data } from "@/packages/<PACKAGE>/data/<DOMAIN>/<DOMAIN><ACTION>Data";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function execute<DOMAIN><ACTION>Service(<PARAMS>) {
  const response = await <DOMAIN><ACTION>Data(<ARGS>);
  return response;
}

export const <DOMAIN><ACTION>Service = withClientErrorHandler(execute<DOMAIN><ACTION>Service);
```

## 2.6 Hook - Read

```ts
import { useCallback, useState } from "react";
import type { <ENTITY_INTERFACE> } from "@/packages/<PACKAGE>/<INTERFACE_DIR>/<DOMAIN>/<ENTITY_INTERFACE_FILE>";
import { <DOMAIN>IndexService } from "@/packages/<PACKAGE>/<SERVICE_DIR>/<DOMAIN>/<DOMAIN>IndexService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const use<DOMAIN>ReadHook = () => {
  const { setResponse } = useResponse();
  const [items, setItems] = useState<<ENTITY_INTERFACE>[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchItems = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await <DOMAIN>IndexService();
      // aplicar estado + setResponse
      return response;
    } finally {
      setIsLoading(false);
    }
  }, [setResponse]);

  return { items, setItems, isLoading, fetchItems };
};
```

## 2.7 Hook - Save

```ts
import { useState } from "react";
import { useResponse } from "@/shared/components/response/ResponseContext";
import { <DOMAIN>SaveCreateService } from "@/packages/<PACKAGE>/<SERVICE_DIR>/<DOMAIN>/<DOMAIN>SaveCreateService";
import { <DOMAIN>SaveUpdateService } from "@/packages/<PACKAGE>/<SERVICE_DIR>/<DOMAIN>/<DOMAIN>SaveUpdateService";

export const use<DOMAIN>SaveHook = () => {
  const { setResponse } = useResponse();
  const [item, setItem] = useState<<ENTITY_INTERFACE> | null>(null);

  const saveItem = async (data: <FORM_VALUES>, selected: <ENTITY_INTERFACE> | null) => {
    const response = selected
      ? await <DOMAIN>SaveUpdateService(selected.<ID_FIELD>, data)
      : await <DOMAIN>SaveCreateService(data);
    setResponse(response);
    return response;
  };

  return { item, saveItem };
};
```

## 2.8 Hook - Delete

```ts
import { useState } from "react";
import { useResponse } from "@/shared/components/response/ResponseContext";
import { <DOMAIN>DeleteService } from "@/packages/<PACKAGE>/<SERVICE_DIR>/<DOMAIN>/<DOMAIN>DeleteService";

export const use<DOMAIN>DeleteHook = () => {
  const { setResponse } = useResponse();
  const [item, setItem] = useState<<ENTITY_INTERFACE>>();

  const deleteItem = async (id: number) => {
    const response = await <DOMAIN>DeleteService({ <ID_FIELD>: id } as <ENTITY_INTERFACE>);
    setItem({ <ID_FIELD>: id } as <ENTITY_INTERFACE>);
    setResponse(response);
    return response;
  };

  return { item, deleteItem };
};
```

## 2.9 Interface

```ts
export interface <ENTITY_INTERFACE> {
  <ID_FIELD>: number;
  // campos de dominio
}
```

## 2.10 Schema (Zod)

```ts
import * as z from "zod";

export const <schemaConstName> = z.object({
  // campos validados
});

export type <SchemaValuesTypeName> = z.infer<typeof <schemaConstName>>;
```

## 2.11 Component - Index

```tsx
"use client";

import { useEffect } from "react";
import { use<DOMAIN>ReadHook } from "@/packages/<PACKAGE>/hooks/<DOMAIN>/use<DOMAIN>ReadHook";

export default function <DOMAIN>Index() {
  const { items, isLoading, fetchItems } = use<DOMAIN>ReadHook();

  useEffect(() => {
    void fetchItems();
  }, [fetchItems]);

  return <div>{/* tabela/filtro/dialog */}</div>;
}
```

## 2.12 App Router - page.tsx

```tsx
import <DOMAIN>Index from "@/packages/<PACKAGE>/components/<DOMAIN>/<DOMAIN>Index";

export default <DOMAIN>Index;
```

Variacao observada para formularios:

```tsx
import { <DOMAIN>Form } from "@/packages/<PACKAGE>/components/<DOMAIN>";
export default function Page() {
  return <<DOMAIN>Form />;
}
```

---

## 3) Regras de validacao automatica

## 3.1 Validacoes de estrutura (gerador)

1. Para cada acao habilitada, validar existencia dos arquivos esperados:
   - `data`, `<service|services>`, `hooks`;
   - `components` para `index` e opcionalmente `form`.
2. Validar que `page.tsx` aponta para componente em `@/packages/...`.
3. Bloquear geracao se `route.path` ja existir e `overwrite = false`.

## 3.2 Validacoes de contrato (AST/regex)

- `data`:
  - deve conter `API` e `Methods`.
  - deve conter `withClientErrorHandler` (wrapper ou chamada protegida).
- `service`:
  - primeira linha com `"use server";`
  - deve chamar apenas `...Data(...)` e retornar response.
- `hooks`:
  - deve importar `useResponse`.
  - deve chamar `setResponse(...)` apos acao assincrona.
  - `use...ShowHook` deve chamar `...ShowService` (nao `IndexService`).
- `schemas`:
  - deve exportar `...Schema` e `z.infer`.
- `interfaces`:
  - deve exportar interface principal do dominio.

## 3.3 Validacao de imports

- nenhum import relativo subindo niveis (`../../../`) em `packages`; usar alias `@/`.
- `app/page.tsx` deve importar de `@/packages` ou `@/components/protesto/route-placeholder`.
- `data` nao pode importar componente React.
- `service` nao pode importar componente React.

## 3.4 Validacao com ferramentas

- lint: `npm run lint`
- tipagem: `npm run typecheck` (se existir script)
- validacao de padrao (custom):
  - `validate-module-standard --package <package> --domain <domain>`

---

## 4) Mapa de roteamento App Router <-> Modulo

## 4.1 Rotas mapeadas para `packages`

| Rota `src/app` | Componente alvo |
| --- | --- |
| `(protected)/cadastro/feriado/page.tsx` | `@/packages/administrativo/components/GFeriado/GFeriadoIndex` |
| `(protected)/cadastro/banco/page.tsx` | `@/packages/administrativo/components/PBanco/PBancoIndex` |
| `(protected)/cadastro/especie/page.tsx` | `@/packages/administrativo/components/PEspecie/PEspecieIndex` |
| `(protected)/cadastro/livro-andamento/page.tsx` | `@/packages/administrativo/components/PLivroAndamento/PLivroAndamentoIndex` |
| `(protected)/cadastro/livro-natureza/page.tsx` | `@/packages/administrativo/components/PLivroNatureza/PLivroNaturezaIndex` |
| `(protected)/cadastro/motivo-apontamento/page.tsx` | `@/packages/administrativo/components/PMotivos/PMotivosIndex` |
| `(protected)/cadastro/motivo-cancelamento/page.tsx` | `@/packages/administrativo/components/PMotivosCancelamento/PMotivosCancelamentoIndex` |
| `(protected)/cadastro/ocorrencias/page.tsx` | `@/packages/administrativo/components/POcorrencias/POcorrenciasIndex` |
| `(protected)/cadastro/pessoas/page.tsx` | `@/packages/administrativo/components/PPessoa/PPessoaIndex` |
| `(protected)/titulos/page.tsx` | `@/packages/administrativo/components/PTitulo` (`PTituloIndex`) |
| `(protected)/titulo/new/page.tsx` | `@/packages/administrativo/components/PTitulo` (`PTituloForm`) |
| `(protected)/titulos/[id]/page.tsx` | `@/packages/administrativo/components/PTitulo` (`PTituloForm`) |
| `(protected)/certidao/page.tsx` | `@/packages/certidao/components/PCertidao/PCertidaoIndex` |
| `(protected)/cra/andamento/page.tsx` | `@/packages/cra/components/PAndamentoCra/PAndamentoCraIndex` |
| `(protected)/cra/confirmacao/page.tsx` | `@/packages/cra/components/PArquivoTitulo/PArquivoTituloIndex` |
| `(protected)/cra/importacao/page.tsx` | `@/packages/cra/components/CraImportacao/CraImportacaoIndex` |
| `(protected)/cra/retorno/page.tsx` | `@/packages/cra/components/PRetornoCra/PRetornoCraIndex` |
| `(protected)/apontamento-lote/page.tsx` | `@/packages/apontamento-lote/components/PTituloApontamentoBatch/PTituloApontamentoBatchIndex` |
| `(protected)/intimacao-lote/page.tsx` | `@/packages/intimacao-lote/components/PTituloIntimacaoBatch/PTituloIntimacaoBatchIndex` |
| `(protected)/protesto-lote/page.tsx` | `@/packages/protesto-lote/components/PTituloProtestarBatch/PTituloProtestarBatchIndex` |

## 4.2 Rotas sem modulo em `packages` (placeholder/dashboard)

| Rota `src/app` | Situacao atual |
| --- | --- |
| `(protected)/integracao/cenprot/page.tsx` | `RoutePlaceholder` |
| `(protected)/integracao/coaf/page.tsx` | `RoutePlaceholder` |
| `(protected)/integracao/serasa/page.tsx` | `RoutePlaceholder` |
| `(protected)/integracao/cenprot-emolumentos/page.tsx` | `RoutePlaceholder` |
| `(protected)/page.tsx` | dashboard local da rota |

## 4.3 Regra executavel de roteamento

Ao gerar novo modulo:

1. criar componente alvo em `src/packages/<package>/components/<Domain>/<Domain>Index.tsx` (ou `Form`);
2. criar `src/app/<group>/<path>/page.tsx` importando o componente do `packages`;
3. registrar no mapa de rotas da documentacao;
4. validar que nao existe rota duplicada apontando para dominio diferente.

---

## 5) Observacoes de compatibilidade

O repositorio possui variacoes historicas em nomes de pasta:

- `service` e `services`
- `interface` e `interfaces`

O schema do agente deve suportar ambos via `folders.serviceDirName` e `folders.interfaceDirName`, evitando quebrar dominios legados e permitindo padronizacao progressiva.
