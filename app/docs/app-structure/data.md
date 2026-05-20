# Data

## Finalidade

A função `GCartorioIndexData` representa um **caso de uso de integração de dados** no frontend, cuja responsabilidade é **buscar a lista de registros da entidade `GCartorio`** diretamente na API.
Ela encapsula a chamada HTTP e fornece um ponto único e padronizado para a obtenção dessas informações, mantendo a lógica de requisição isolada da interface e dos componentes de aplicação.

---

## Responsabilidades

* Realizar uma requisição HTTP do tipo **GET** para o endpoint `administrativo/g_cartorio/`.
* Utilizar a classe `API` como camada de abstração de requisições, mantendo a padronização do projeto.
* Retornar uma resposta padronizada no formato `ApiResponseInterface`.
* Garantir o tratamento global de erros no cliente por meio do wrapper `withClientErrorHandler`.

---

## Características Técnicas

* Implementada como uma **função assíncrona** que realiza chamadas HTTP com métodos e endpoints configuráveis.
* Utiliza a enum `Methods` para garantir consistência na definição do método HTTP.
* É encapsulada pela função `withClientErrorHandler`, que fornece um middleware de tratamento de erros, logs e mensagens ao usuário.
* Opera na camada de **data**, responsável pela comunicação direta com a API.
* Retorna a resposta bruta da requisição, sem aplicar formatação ou transformação de dados — responsabilidade da camada de `services`.

---

## Código

```typescript
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';
import ApiResponseInterface from '@/shared/services/api/interfaces/ApiResponseInterface';

async function executeGCartorioIndexData(): Promise<ApiResponseInterface> {
  // Instancia o cliente HTTP padronizado
  const api = new API();

  // Executa a requisição para o endpoint de listagem de cartórios
  return api.send({
    method: Methods.GET,
    endpoint: `administrativo/g_cartorio/`,
  });
}

// Encapsula a função com o manipulador de erros do cliente
export const GCartorioIndexData = withClientErrorHandler(executeGCartorioIndexData);
```

---

## Fluxo de Execução

1. O componente ou hook chama `GCartorioIndexData()`.
2. A função realiza a requisição HTTP via `API.send()`.
3. Em caso de sucesso, retorna um objeto compatível com `ApiResponseInterface`.
4. Em caso de erro, o `withClientErrorHandler` captura e trata o problema, exibindo mensagens adequadas e mantendo a aplicação estável.

---

## Conclusão

O `GCartorioIndexData` é um componente essencial da camada de **integração de dados** no frontend.
Ele fornece um ponto único, padronizado e seguro para buscar informações do backend, garantindo isolamento da infraestrutura, reutilização de código e consistência na comunicação entre camadas.