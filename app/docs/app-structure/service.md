# Service

## Finalidade

O **`GCartorioIndexService`** representa um **serviço de orquestração de dados** do domínio `GCartorio`.
Sua responsabilidade é **intermediar a camada de integração (`data`) e a camada de aplicação (`hooks`)**, garantindo um fluxo consistente, seguro e padronizado para a obtenção de registros de cartórios.

---

## Responsabilidades

* Executar o caso de uso definido em `GCartorioIndexData`, responsável pela chamada direta à API.
* Centralizar a resposta da operação e repassá-la de forma transparente à camada de aplicação.
* Garantir o tratamento global de erros no cliente através do wrapper `withClientErrorHandler`.
* Servir como ponto de entrada padronizado para qualquer parte do sistema que precise consultar dados do domínio `GCartorio`.

---

## Características Técnicas

* Implementado como uma **função assíncrona**, responsável por orquestrar a execução de `GCartorioIndexData`.
* Encapsulado pelo **decorator `withClientErrorHandler`**, que adiciona camadas automáticas de tratamento de erros e feedback ao usuário.
* Atua na camada de **service**, segundo os princípios da **Clean Architecture**, isolando a lógica de aplicação da infraestrutura de rede.
* Retorna a resposta bruta da camada `data`, permitindo que a camada `hook` decida como manipulá-la.
* Possui estrutura simples, reutilizável e coerente com o padrão de serviços de outros domínios.

---

## Código

```typescript
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import { GCartorioIndexData } from '../../data/GCartorio/GCartorioIndexData';

async function executeGCartorioIndexService() {
  // Executa a função de integração com a API
  const response = await GCartorioIndexData();

  // Retorna o resultado da requisição
  return response;
}

// Encapsula com o tratador de erros do cliente
export const GCartorioIndexService = withClientErrorHandler(executeGCartorioIndexService);
```

---

## Fluxo de Execução

1. O `hook` chama o `GCartorioIndexService()` para buscar os registros.
2. O serviço executa `GCartorioIndexData()`, que realiza a requisição HTTP à API.
3. O resultado é retornado para o `hook`, mantendo o formato padronizado.
4. Se ocorrer qualquer erro, o `withClientErrorHandler` intercepta, trata e exibe mensagens adequadas ao usuário.

---

## Conclusão

O **`GCartorioIndexService`** é um componente essencial da **camada de serviços de domínio**,
atuando como **ponte entre a integração de dados e a lógica de aplicação**.
Ele garante **tratamento centralizado de erros**, **padronização de respostas** e **isolamento arquitetural**,
seguindo fielmente os princípios de **Clean Architecture** e **Single Responsibility** no frontend.