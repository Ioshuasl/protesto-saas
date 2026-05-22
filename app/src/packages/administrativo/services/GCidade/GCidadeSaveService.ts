'use server';

import { GCidadeSaveData } from '@/packages/administrativo/data/GCidade/GCidadeSaveData';
import GCidadeInterface from '@/packages/administrativo/interfaces/GCidade/GCidadeInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

// Função assíncrona que executa o salvamento de uma cidade
async function executeGCidadeSaveService(data: GCidadeInterface) {
  // Chama a função que salva os dados da cidade
  const response = await GCidadeSaveData(data);

  // Retorna a resposta do salvamento
  return response;
}

// Exporta o serviço de salvamento de cidade já encapsulado com tratamento de erros
export const GCidadeSaveService = withClientErrorHandler(executeGCidadeSaveService);
