# Interface

## Finalidade

A **`GCartorioInterface`** define a **estrutura tipada do domínio `GCartorio`**,
servindo como **contrato de dados** entre as camadas da aplicação frontend.
Ela descreve todas as propriedades esperadas de um registro de cartório, garantindo **consistência, segurança de tipos e previsibilidade** no fluxo de informações.

---

## Responsabilidades

* Representar o modelo de dados do domínio `GCartorio` em formato **TypeScript Interface**.
* Padronizar os tipos de dados utilizados em formulários, hooks, serviços e componentes.
* Assegurar a coerência entre o frontend e o backend, refletindo os campos do banco de dados ou do schema da API.
* Permitir **autocompletar, validação de tipo e segurança em tempo de compilação**, reduzindo erros de integração.

---

## Características Técnicas

* Implementada como uma **interface TypeScript**, sem dependência de bibliotecas externas.
* Todos os campos são opcionais (`?`), permitindo uso flexível em operações **CRUD** (criação, leitura, atualização, exclusão).
* Inclui propriedades de diferentes naturezas — identificadores, dados cadastrais, endereços, contatos e informações funcionais.
* É amplamente utilizada em:

  * **Schemas (Zod)** — para validação e tipagem inferida.
  * **Hooks** — para tipar estados e parâmetros de funções assíncronas.
  * **Services** — para garantir integridade nos dados enviados ou recebidos.
  * **Componentes** — para tipagem de props e formulários dinâmicos.

---

## Código

```typescript
export default interface GCartorioInterface {
  cartorio_id?: number;
  seq?: string;
  cns?: string;
  cnpj?: string;
  denominacao_serventia?: string;
  status_serventia?: number;
  atribuicao?: string;
  ...
}
```

---

## Fluxo de Utilização

1. A interface é importada por **hooks** (ex: `useGCartorioIndexHook`, `useGCartorioSaveHook`) para tipar estados e parâmetros.
2. Os **schemas** (`GCartorioSchema`) baseiam-se nela para manter a coerência entre validação e modelo.
3. Os **services** (`GCartorioIndexService`, `GCartorioSaveService`) utilizam o tipo para garantir compatibilidade entre o backend e o frontend.
4. Os **componentes** (`GCartorioForm`, `GCartorioTable`) consomem objetos que seguem essa interface.

---

## Conclusão

A **`GCartorioInterface`** é a **base de tipagem do domínio GCartorio** e garante que todos os módulos do frontend —
dos serviços à interface — mantenham **consistência estrutural, segurança de tipo e clareza semântica**.
Ela é um dos pilares da arquitetura orientada a domínio (DDD) aplicada ao frontend,
sendo essencial para a **manutenibilidade, escalabilidade e confiabilidade** do sistema.