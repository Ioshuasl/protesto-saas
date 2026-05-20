'use server';

import { PLivroAndamentoSaveCreateData } from '@/packages/administrativo/data/PLivroAndamento/PLivroAndamentoSaveData';
import type { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroAndamentoSaveCreateService(
  data: Omit<PLivroAndamentoInterface, 'livro_andamento_id'>,
) {
  const response = await PLivroAndamentoSaveCreateData(data);

  return response;
}

export const PLivroAndamentoSaveCreateService = withClientErrorHandler(
  executePLivroAndamentoSaveCreateService,
);
