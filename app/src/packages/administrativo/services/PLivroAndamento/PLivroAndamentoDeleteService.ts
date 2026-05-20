'use server';

import { PLivroAndamentoDeleteData } from '@/packages/administrativo/data/PLivroAndamento/PLivroAndamentoDeleteData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroAndamentoDeleteService(id: number) {
  const response = await PLivroAndamentoDeleteData(id);

  return response;
}

export const PLivroAndamentoDeleteService = withClientErrorHandler(executePLivroAndamentoDeleteService);
