'use server';
import { GCidadeIndexData } from '@/packages/administrativo/data/GCidade/GCidadeIndexData';
import GCidadeInterface from '@/packages/administrativo/interfaces/GCidade/GCidadeInterface'; // Interface tipada da cidade
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

// Função assíncrona que executa a chamada para buscar os dados de cidades
async function executeGCidadeIndexService(data: GCidadeInterface) {
  // Chama a função que retorna os dados da cidade
  const response = await GCidadeIndexData(data);

  // Retorna a resposta para o chamador
  return response;
}

// Exporta o serviço de índice de cidades já encapsulado com tratamento de erros
export const GCidadeIndexService = withClientErrorHandler(executeGCidadeIndexService);
