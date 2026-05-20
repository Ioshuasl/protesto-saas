# Pacotes

# Visão Geral da Estrutura de Pacotes

```text
packages/
└── administrativo/
    ├── components/     # Camada de interface (UI)
    ├── hooks/          # Casos de uso e lógica de aplicação
    ├── services/       # Regras de orquestração de dados (chamada dos data)
    ├── data/           # Serviços de integração com API
    ├── interfaces/     # Tipagem e contratos de dados (Domain Layer)
    ├── schemas/        # Validações e estruturas com Zod
```

Cada diretório representa uma **camada arquitetural independente**, que se comunica com as outras de forma controlada.
Essa organização segue os princípios de **Clean Architecture aplicada ao frontend**, onde a dependência sempre aponta do **externo (UI)** para o **interno (domínio e dados)**.

---

## Estrutura Modular

Cada módulo (como `GCartorio`, `GNatureza`, `TPessoa`, `TImovel`) é um **microdomínio isolado** que contém tudo o que precisa para funcionar.
Essa independência garante **reutilização, testabilidade e baixo acoplamento**, conceitos centrais de um **Monolito Modular**.

---

## Explicação por Diretório e Responsabilidade

### `interfaces/` — Camada de Domínio

Define as **estruturas e contratos de dados** que representam o modelo do negócio no frontend.
É a camada mais estável, utilizada por todas as demais camadas.

---

### `schemas/` — Camada de Validação

Define os **schemas Zod** para validação de formulários e tipagem de entrada e saída de dados.
Garante consistência e segurança na manipulação das informações.

---

### `data/` — Camada de Infraestrutura

Responsável pela **comunicação direta com a API**.
Centraliza as requisições HTTP e abstrai o acesso ao backend.
Não contém regras de negócio, apenas a integração técnica.

---

### `services/` — Camada de Orquestração de Dados

Orquestra as chamadas aos `data`, realiza formatações e aplica regras de negócio do frontend.
Funciona como os casos de uso (use cases), transformando dados brutos em informações utilizáveis pela aplicação.

---

### `hooks/` — Camada de Aplicação

Encapsula o fluxo de dados e lógica da aplicação.
Gerencia estados, executa os serviços e retorna dados e handlers prontos para uso na interface.

---

### `components/` — Camada de Interface (UI Layer)

Responsável por **renderizar telas, formulários, tabelas e interações visuais**.
É a camada mais externa, conectada aos hooks e independente da lógica interna.

---

## Relação entre as Camadas

| Camada         | Responsabilidade    | Exemplo de Dependência        |
| -------------- | ------------------- | ----------------------------- |
| **components** | Renderização e UI   | usa → `hooks`                 |
| **hooks**      | Lógica e estado     | usa → `services`              |
| **services**   | Regras e formatação | usa → `data`                  |
| **data**       | Comunicação com API | usa → `interfaces`            |
| **schemas**    | Validação           | usada em `forms` e `services` |
| **interfaces** | Tipagem base        | usada em todas as camadas     |

**Fluxo completo:**

```
UI (Component) → Hook → Service → Data → API → (Response) → Service → UI
```

---

## Vantagens da Estrutura

* Modularidade e isolamento entre domínios.
* Reutilização de código e padrões consistentes.
* Escalabilidade para novos módulos sem retrabalho.
* Facilidade de manutenção e testes.
* Possibilidade de trabalho paralelo entre equipes.

---

## Conclusão

O diretório `packages/administrativo` representa uma **arquitetura modular de frontend orientada a domínio**,
onde cada módulo funciona como um **contexto independente**, e todas as camadas seguem a regra de fluxo:

> **Domínio → Aplicação → Interface**

Essa estrutura combina **DDD**, **Clean Architecture**, **SOLID** e **Monolito Modular**,
resultando em um **frontend corporativo robusto, escalável e de fácil evolução**.