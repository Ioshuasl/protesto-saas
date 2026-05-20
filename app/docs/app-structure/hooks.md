# Hooks

## Finalidade

O **`useGCartorioIndexHook`** é um **hook de aplicação** responsável por **gerenciar a listagem de registros do domínio `GCartorio`**.
Ele encapsula o fluxo completo de **requisição, armazenamento e resposta**, conectando a camada de serviços (`GCartorioIndexService`) à interface de usuário.

---

## Responsabilidades

* Solicitar os dados de cartórios por meio do `GCartorioIndexService`.
* Armazenar a lista de registros localmente no estado do componente (`useState`).
* Integrar-se ao contexto global de respostas (`useResponse`) para exibir feedbacks visuais (toasts, modais, alertas, etc.).
* Fornecer os dados e a função de atualização (`indexGCartorio`) para os componentes que consomem o hook.

---

## Características Técnicas

* Implementado como um **React Hook** padrão (`useState`, `useResponse`).
* Funciona como uma ponte entre a camada de **serviço** e a **interface (componentes React)**.
* Segue os princípios de **Clean Architecture**, mantendo a lógica de aplicação isolada da infraestrutura e da UI.
* Retorna um **estado reativo** com a lista de registros e uma **função assíncrona** para atualização dos dados.
* Utiliza **tipagem forte** com `GCartorioInterface` para garantir segurança e consistência dos dados manipulados.

---

## Código

```typescript
'use client';

import { useState } from 'react';
import { useResponse } from '@/shared/components/response/ResponseContext';

import GCartorioInterface from '../../interfaces/GCartorio/GCartorioInterface';
import { GCartorioIndexService } from '../../services/GCartorio/GCartorioIndexService';

export const useGCartorioIndexHook = () => {
  // Contexto global de respostas e feedbacks
  const { setResponse } = useResponse();

  // Estado local que armazena os registros
  const [gGramatica, setGCartorio] = useState<GCartorioInterface[]>([]);

  // Função de listagem dos registros
  const indexGCartorio = async () => {
    const response = await GCartorioIndexService();

    // Atualiza os dados locais
    setGCartorio(response.data);

    // Define a resposta global (toast, modal, alerta, etc.)
    setResponse(response);
  };

  return {
    gGramatica,
    indexGCartorio,
  };
};
```

---

## Fluxo de Execução

1. O hook é importado e chamado dentro de um componente (ex: `GCartorioIndex`).
2. Ao invocar `indexGCartorio()`, o hook solicita os dados via `GCartorioIndexService`.
3. Os registros retornados são armazenados no estado interno (`setGCartorio`).
4. A resposta é enviada ao contexto global (`setResponse`) para gerar feedbacks visuais.
5. Os componentes que consomem o hook recebem a lista atualizada (`gGramatica`).

---

## Conclusão

O **`useGCartorioIndexHook`** é um **caso de uso de frontend** que centraliza a lógica de obtenção e gerenciamento de dados da entidade `GCartorio`.
Ele garante **isolamento de responsabilidades**, **consistência de estado** e **integração fluida** entre as camadas de serviço, domínio e interface — seguindo os princípios da **Clean Architecture** e **Single Responsibility** no frontend.