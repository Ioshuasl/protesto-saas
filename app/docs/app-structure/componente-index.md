# Componente Index

## Finalidade

O componente `GCartorioIndex` representa a **camada de interface de listagem e controle** do domínio `GCartorio`.
Sua função é **centralizar o fluxo de exibição, criação, edição e exclusão** de registros, orquestrando a interação entre a interface, os hooks e os serviços de dados.

---

## Responsabilidades

* Exibir a listagem principal dos registros de cartórios.
* Controlar a abertura e fechamento do formulário de criação/edição.
* Coordenar a exclusão de registros por meio de um **diálogo de confirmação**.
* Integrar os hooks de leitura (`useGCartorioIndexHook`), gravação (`useGCartorioSaveHook`) e exclusão (`useGCartorioDeleteHook`).
* Gerenciar o estado local da interface, como o item selecionado, carregamento de botões e modais abertos.
* Atualizar automaticamente a listagem após operações de criação, edição ou exclusão.

---

## Características Técnicas

* Implementado como um **Client Component** (`'use client'`), executado no lado do cliente.
* Utiliza **React Hooks** (`useState`, `useEffect`, `useCallback`) para controle de estado e efeitos colaterais.
* Segue o padrão de **Clean Architecture no frontend**, isolando responsabilidades entre camadas:

  * `hooks` → encapsulam a lógica de aplicação e comunicação com o backend.
  * `components` → lidam exclusivamente com exibição e interação do usuário.
* Possui **integração modular**, reutilizando componentes compartilhados:

  * `Header` para título e botão de criação.
  * `GCartorioForm` para formulário de cadastro/edição.
  * `GCartorioTable` para listagem.
  * `ConfirmDialog` para confirmação de exclusão.
  * `Loading` para estados de carregamento.
* Mantém o **estado global local ao componente**, garantindo previsibilidade e independência.
* Reaproveita hooks específicos do domínio `GCartorio`, mantendo consistência e padronização com outros módulos do sistema.

---

## Fluxo de Execução

1. Ao carregar o componente, a listagem é obtida automaticamente via `useGCartorioIndexHook`.
2. O botão “Novo Cartório” abre o formulário de criação.
3. A ação “Editar” na tabela reabre o formulário com os dados selecionados.
4. A ação “Excluir” abre o diálogo de confirmação.
5. Após confirmação, o hook `useGCartorioDeleteHook` executa a remoção e a listagem é atualizada.
6. Em qualquer operação (criar, editar, excluir), o componente mantém a interface sincronizada com os dados.

---

## Integração Arquitetural

O `GCartorioIndex` atua como **controlador de fluxo da interface**, conectando as camadas:

| Camada   | Elemento utilizado       | Função principal                       |
| -------- | ------------------------ | -------------------------------------- |
| **Hook** | `useGCartorioIndexHook`  | Buscar registros e atualizar listagem. |
| **Hook** | `useGCartorioSaveHook`   | Criar ou atualizar registros.          |
| **Hook** | `useGCartorioDeleteHook` | Remover registros existentes.          |
| **UI**   | `GCartorioForm`          | Exibir e validar dados de entrada.     |
| **UI**   | `GCartorioTable`         | Exibir registros e ações de interação. |
| **UI**   | `ConfirmDialog`          | Confirmar operações destrutivas.       |
| **UI**   | `Header`, `Loading`      | Estrutura e estados de carregamento.   |

---

## Conclusão

O `GCartorioIndex` é o ponto central da **interação do usuário com o domínio GCartorio**,
seguindo uma estrutura modular, reativa e desacoplada, em conformidade com os princípios de **Clean Architecture**, **Single Responsibility** e **Domain-Driven Design** no frontend.