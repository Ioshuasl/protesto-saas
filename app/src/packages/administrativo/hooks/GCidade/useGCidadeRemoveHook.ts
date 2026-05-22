import { GCidadeRemoveData } from '@/packages/administrativo/data/GCidade/GCidadeRemoveData'; // Função que remove a cidade via API
import GCidadeInterface from '@/packages/administrativo/interfaces/GCidade/GCidadeInterface'; // Interface tipada da cidade
import { useResponse } from '@/shared/components/response/ResponseContext'; // Contexto global para gerenciar respostas da API

// Hook customizado para remoção de cidades
export const useGCidadeRemoveHook = () => {
  // Hook do contexto de resposta para feedback global (alertas, mensagens etc.)
  const { setResponse } = useResponse();

  // Função assíncrona que remove uma cidade
  const removeGCidade = async (data: GCidadeInterface) => {
    // Chama a função de remoção passando os dados da cidade
    const response = await GCidadeRemoveData(data);

    // Atualiza o contexto global com a resposta da API
    setResponse(response);
  };

  // Retorna a função de remoção para ser usada no componente
  return { removeGCidade };
};
