'use server';

import {
  PLivroAndamentoSaveCreateData,
  type PLivroAndamentoSavePayload,
} from '@/packages/administrativo/data/PLivroAndamento/PLivroAndamentoSaveData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroAndamentoSaveCreateService(data: PLivroAndamentoSavePayload) {
  const response = await PLivroAndamentoSaveCreateData(data);

  return response;
}

export const PLivroAndamentoSaveCreateService = withClientErrorHandler(
  executePLivroAndamentoSaveCreateService,
);
