'use server';

import { PLivroAndamentoIndexData } from '@/packages/administrativo/data/PLivroAndamento/PLivroAndamentoIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroAndamentoIndexService() {
  const response = await PLivroAndamentoIndexData();

  return response;
}

export const PLivroAndamentoIndexService = withClientErrorHandler(executePLivroAndamentoIndexService);
