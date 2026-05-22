'use server';
// Função que envolve qualquer ação assíncrona para capturar e tratar erros do cliente
import { GCidadeRemoveData } from '@/packages/administrativo/data/GCidade/GCidadeRemoveData';
// Função que remove os dados da cidade via API
import GCidadeInterface from '@/packages/administrativo/interfaces/GCidade/GCidadeInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
// Interface tipada da cidade

// Função assíncrona que executa a remoção de uma cidade
async function executeGCidadeRemoveService(data: GCidadeInterface) {
  // Chama a função que remove os dados da cidade
  const response = await GCidadeRemoveData(data);

  // Retorna a resposta da remoção
  return response;
}

// Exporta o serviço de remoção de cidade já encapsulado com tratamento de erros
export const GCidadeRemoveService = withClientErrorHandler(executeGCidadeRemoveService);
