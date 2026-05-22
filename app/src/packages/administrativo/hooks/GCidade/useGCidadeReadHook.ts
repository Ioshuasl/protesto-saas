import { useState } from 'react';

import GCidadeInterface from '@/packages/administrativo/interfaces/GCidade/GCidadeInterface'; // Interface tipada da cidade
import { GCidadeIndexService } from '@/packages/administrativo/services/GCidade/GCidadeIndexService'; // Serviço que busca a lista de cidades
import { useResponse } from '@/shared/components/response/ResponseContext'; // Contexto global para gerenciar respostas da API

// Hook customizado para leitura de dados de cidades
export const useGCidadeReadHook = () => {
  // Hook do contexto de resposta para feedback global (alertas, mensagens etc.)
  const { setResponse } = useResponse();

  // Estado local que armazena a lista de cidades retornada da API
  const [gCidade, setGCidade] = useState<GCidadeInterface[]>([]);

  // Função assíncrona que busca os dados de cidades
  const fetchGCidade = async (data: GCidadeInterface) => {
    // Chama o serviço responsável por consultar a API
    const response = await GCidadeIndexService(data);

    // Atualiza o estado local com os dados retornados
    setGCidade(response.data);

    // Atualiza o contexto global de resposta
    setResponse(response);

    // Retorna a resposta para quem chamou o hook
    return response;
  };

  // Retorna os dados e a função de busca para serem usados no componente
  return { gCidade, fetchGCidade };
};
