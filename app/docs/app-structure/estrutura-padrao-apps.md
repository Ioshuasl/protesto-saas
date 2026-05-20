# Estrutura Padrão dos Apps (React + Next.js)

## Objetivo

Este documento consolida o padrão estrutural adotado nos projetos `saas-app` e `protesto-saas-app`, com foco especial na arquitetura de `src/packages`.

A proposta é manter uma base única de organização para:

- escalar novos módulos com baixo acoplamento;
- manter previsibilidade entre equipes;
- facilitar manutenção, testes e evolução contínua.

---

## Visão Geral

Ambos os projetos seguem a mesma espinha dorsal em `src`:

```text
src/
├── app/
├── components/
├── hooks/
├── lib/
├── packages/
└── shared/
```

Mesmo quando os domínios de negócio mudam (administrativo cartorial no `saas-app` e protesto no `protesto-saas-app`), a arquitetura permanece a mesma.

---

## Papel de Cada Pasta em `src`

### `app/` - Rotas e páginas (Next App Router)

Camada responsável por páginas, layouts e segmentação de rotas (`(protected)`, `(public)`), com foco na navegação da aplicação.

Responsabilidades:

- definir entradas de rota (`page.tsx`, `layout.tsx`, `loading.tsx`);
- organizar áreas protegidas e públicas;
- compor telas com componentes de domínio vindos de `packages`.

Observação: alterações de fluxo funcional costumam começar aqui, pois é o ponto de entrada da navegação.

### `components/` - UI reutilizável e estrutura visual global

Camada de componentes compartilhados de interface, incluindo biblioteca base (`ui/`, padrão shadcn) e componentes globais de shell/navegação.

Responsabilidades:

- padronização visual;
- componentes genéricos independentes de domínio;
- composição de layout global da aplicação.

### `hooks/` - Hooks utilitários globais

Hooks transversais usados fora de um domínio específico (ex.: detecção mobile, refs, efeitos utilitários).

### `lib/` - Utilitários centrais de baixo nível

Atualmente abriga utilitários base como `utils.ts` e função `cn`, usados por UI e composição de classes.

### `packages/` - Núcleo modular por domínio (camadas arquiteturais)

É o coração funcional do sistema. Cada módulo de negócio é isolado e implementado com camadas bem definidas.

### `shared/` - Reuso transversal entre apps e domínios

Contém ações, componentes, enums, schemas, hooks, interfaces e serviços utilitários compartilháveis por toda a aplicação (e por futuras aplicações).

---

## Acoplamento Estrutural Intencional: `app` <-> `packages`

Nos nossos apps, existe um acoplamento estrutural intencional entre `src/app` (Next App Router) e os módulos de `src/packages`.

Esse acoplamento nao e de implementacao direta entre camadas internas, e sim de organizacao e fluxo funcional:

- `app` define a arvore de rotas e o contexto de navegacao;
- cada rota/pagina de negocio deve apontar para um modulo correspondente em `packages`;
- a evolucao de rotas em `app` normalmente exige evolucao sincronizada do modulo em `packages`;
- a evolucao de um microdominio em `packages` normalmente exige ajuste de entrada/composicao em `app`.

Em outras palavras: `app` e a porta de entrada do fluxo, e `packages` e a implementacao modular do dominio exposto por esse fluxo.

### Regra pratica de mapeamento

Para cada funcionalidade de negocio publicada no App Router:

1. existe uma rota em `src/app/.../page.tsx`;
2. existe um componente indice de dominio em `src/packages/.../components/...Index.tsx`;
3. esse componente consome `hooks -> services -> data` do mesmo microdominio.

### Exemplo de espelhamento (conceitual)

```text
src/app/(protected)/cadastro/feriado/page.tsx
  -> src/packages/administrativo/components/GFeriado/GFeriadoIndex.tsx
     -> hooks/GFeriado/*
     -> services/GFeriado/*
     -> data/GFeriado/*
```

### Exemplos reais do projeto (`protesto-saas-app`)

Os arquivos abaixo existem no projeto e mostram o acoplamento estrutural na prática:

#### Exemplo 1 - Cadastro de Feriado

```text
src/app/(protected)/cadastro/feriado/page.tsx
  -> importa e exporta: GFeriadoIndex
  -> src/packages/administrativo/components/GFeriado/GFeriadoIndex.tsx
      -> useGFeriadoReadHook / useGFeriadoSaveHook / useGFeriadoDeleteHook
      -> src/packages/administrativo/hooks/GFeriado/useGFeriadoReadHook.ts
          -> GFeriadoIndexService
          -> src/packages/administrativo/services/GFeriado/GFeriadoIndexService.ts
              -> GFeriadoIndexData
              -> src/packages/administrativo/data/GFeriado/GFeriadoIndexData.ts
```

#### Exemplo 2 - Cadastro de Banco

```text
src/app/(protected)/cadastro/banco/page.tsx
  -> importa e exporta: PBancoIndex
  -> src/packages/administrativo/components/PBanco/PBancoIndex.tsx
      -> hooks/PBanco/*
      -> services/PBanco/*
      -> data/PBanco/*
```

#### Exemplo 3 - Títulos (listagem principal)

```text
src/app/(protected)/titulos/page.tsx
  -> renderiza: <PTituloIndex />
  -> src/packages/administrativo/components/PTitulo/PTituloIndex.tsx
      -> hooks/PTitulo/*
      -> services/PTitulo/*
      -> data/PTitulo/*
```

#### Exemplo 4 - CRA / Retorno

```text
src/app/(protected)/cra/retorno/page.tsx
  -> renderiza: <PRetornoCraIndex />
  -> src/packages/cra/components/PRetornoCra/PRetornoCraIndex.tsx
      -> hooks/PRetornoCra/*
      -> service/PRetornoCra/*
      -> data/PRetornoCra/*
```

Esses exemplos mostram que o App Router nao apenas "aponta" para componentes; ele organiza os contextos de negocio que sao implementados em `packages` com o mesmo recorte funcional.

### Implicacao arquitetural

Ao criar, mover ou renomear rotas em `src/app`, validar sempre:

- se o modulo correspondente em `src/packages` existe e segue o padrao;
- se os nomes de dominio continuam consistentes entre rota, componente indice e camadas internas;
- se o fluxo da rota ainda respeita a cadeia `components -> hooks -> services -> data`.

Esse alinhamento e parte do padrao oficial dos projetos.

---

## Estrutura de `packages` (Padrão Oficial)

```text
packages/
└── administrativo/
    ├── components/     # Interface do domínio
    ├── hooks/          # Lógica de aplicação e casos de uso no client
    ├── services/       # Orquestração e regra de negócio
    ├── data/           # Integração externa (API, mock, adapters)
    ├── interfaces/     # Contratos e tipagens de domínio
    └── schemas/        # Validação (Zod)
```

Essa organização implementa princípios de Clean Architecture no frontend, com separação clara entre:

- **camada de apresentação**;
- **camada de aplicação/orquestração**;
- **camada de dados/infra**;
- **contratos de domínio e validação**.

---

## Responsabilidades por Camada em `packages`

### `interfaces/` (Domínio e contratos)

- define formatos de entidade e contratos de dados;
- base tipada consumida pelas demais camadas;
- deve ser estável e agnóstica de UI.

### `schemas/` (Validação e consistência)

- define schemas Zod para formulários e payloads;
- protege fronteiras de entrada/saída;
- pode ser usada em hooks, forms e serviços.

### `data/` (Integração externa)

- executa comunicação direta com API (ou mock/in-memory no ambiente local);
- não deve conter regra de negócio;
- foca em transporte de dados.

### `services/` (Orquestração e regra)

- coordena chamadas de `data`;
- aplica transformação, composição e regra de negócio;
- entrega dados prontos para consumo da aplicação.

### `hooks/` (Aplicação no client)

- gerencia estado, ciclo de vida e side-effects de tela;
- conecta UI aos serviços;
- expõe handlers e estado para `components`.

### `components/` (UI do domínio)

- renderiza telas, forms, tabelas e diálogos do módulo;
- aciona hooks para comportamento;
- evita regra de negócio pesada dentro do componente.

---

## Regra de Dependência entre Camadas

Dependência recomendada (externo para interno):

```text
components -> hooks -> services -> data
                       ↘
                interfaces / schemas
```

Fluxo típico ponta a ponta:

```text
UI (Component)
  -> Hook
    -> Service
      -> Data
        -> API
      <- resposta normalizada
    <- estado/handlers
<- renderização
```

Diretriz importante:

- `data` não conhece UI;
- `services` não deve depender de componente React;
- `components` não deve chamar API diretamente.

---

## Microdomínios em `packages`

Cada pasta de módulo (ex.: `GCartorio`, `GFeriado`, `PTitulo`, `TPessoa`) funciona como um microdomínio isolado, contendo seu próprio conjunto de:

- componentes;
- hooks;
- serviços;
- integração de dados;
- contratos e validações.

Benefícios diretos:

- evolução independente por domínio;
- menor risco de regressão cruzada;
- maior clareza para onboarding e code review.

---

## Como o Padrão Aparece nos Dois Projetos

## `saas-app`

- possui forte cobertura de módulos administrativos e de serviços cartoriais;
- grande quantidade de módulos maduros em `packages/administrativo`;
- padronização já consolidada de sufixos (`Index`, `Save`, `Delete`, `Show`, etc.).

## `protesto-saas-app`

- mantém a mesma base estrutural;
- aplica o padrão para novos contextos de protesto (`PBanco`, `POcorrencias`, `PTitulo`, `CraImportacao`, lotes etc.);
- combina integração real e estratégias in-memory em alguns `data`, preservando a mesma arquitetura.

Conclusão: muda o domínio, não muda a arquitetura.

---

## Convenções de Nomenclatura (Prática Atual)

Padrões observados e recomendados:

- `XxxIndexData`, `XxxSaveData`, `XxxDeleteData`, `XxxShowData` em `data`;
- `XxxIndexService`, `XxxSaveService` em `services`;
- `useXxxReadHook`, `useXxxSaveHook`, `useXxxDeleteHook` em `hooks`;
- `XxxFormSchema` em `schemas`;
- `XxxInterface` em `interfaces`;
- `XxxIndex`, `XxxTable`, `XxxForm`, `XxxDialog` em `components`.

Isso facilita descoberta por busca, consistência entre módulos e automação futura.

---

## Guia de Criação de Novo Módulo

Ao criar um novo módulo em `packages`, seguir o checklist:

1. Criar contrato em `interfaces`.
2. Criar validações em `schemas`.
3. Implementar integração em `data`.
4. Implementar regras/orquestração em `services`.
5. Criar hooks de aplicação (`read`, `save`, `delete`, etc.).
6. Montar componentes de UI (index/tabela/form/dialog).
7. Conectar rota em `app` para disponibilizar a tela.

---

## Boas Práticas Arquiteturais

- manter cada arquivo com responsabilidade única;
- evitar acoplamento cruzado entre microdomínios;
- centralizar regra de negócio em `services`;
- validar entradas com `schemas` nas fronteiras;
- usar `shared` apenas para itens realmente transversais.

Antipadrões a evitar:

- chamar API diretamente em componente;
- replicar tipagens em vez de usar `interfaces`;
- colocar regra de negócio dentro de `data`;
- criar utilitário de domínio em `shared` sem necessidade real de reuso.

---

## Resultado Esperado com Este Padrão

- crescimento sustentável dos apps;
- código mais previsível e revisável;
- facilidade para reaproveitar blocos entre produtos;
- menor custo de manutenção de longo prazo.

Em resumo, `saas-app` e `protesto-saas-app` compartilham um blueprint arquitetural único para frontend corporativo modular, orientado a domínio e pronto para evolução contínua.
