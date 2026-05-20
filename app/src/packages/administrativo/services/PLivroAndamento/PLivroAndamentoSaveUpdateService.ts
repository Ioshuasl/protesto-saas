'use server';

import { PLivroAndamentoSaveUpdateData } from '@/packages/administrativo/data/PLivroAndamento/PLivroAndamentoSaveData';
import type { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroAndamentoSaveUpdateService(
  id: number,
  data: Partial<PLivroAndamentoInterface>,
) {
  const response = await PLivroAndamentoSaveUpdateData(id, data);

  return response;
}

export const PLivroAndamentoSaveUpdateService = withClientErrorHandler(
  executePLivroAndamentoSaveUpdateService,
);
