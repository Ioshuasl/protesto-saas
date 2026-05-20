'use server';

import { PLivroAndamentoShowData } from '@/packages/administrativo/data/PLivroAndamento/PLivroAndamentoShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroAndamentoShowService(id: number) {
  const response = await PLivroAndamentoShowData(id);

  return response;
}

export const PLivroAndamentoShowService = withClientErrorHandler(executePLivroAndamentoShowService);
