'use server';

import {
  PLivroAndamentoSaveUpdateData,
  type PLivroAndamentoSavePayload,
} from '@/packages/administrativo/data/PLivroAndamento/PLivroAndamentoSaveData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroAndamentoSaveUpdateService(
  id: number,
  data: Partial<PLivroAndamentoSavePayload>,
) {
  const response = await PLivroAndamentoSaveUpdateData(id, data);

  return response;
}

export const PLivroAndamentoSaveUpdateService = withClientErrorHandler(
  executePLivroAndamentoSaveUpdateService,
);
