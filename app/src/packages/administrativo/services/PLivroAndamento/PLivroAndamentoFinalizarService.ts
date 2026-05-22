'use server';

import {
  PLivroAndamentoFinalizarData,
  type PLivroAndamentoFinalizarPayload,
} from '@/packages/administrativo/data/PLivroAndamento/PLivroAndamentoFinalizarData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroAndamentoFinalizarService(
  id: number,
  data: PLivroAndamentoFinalizarPayload,
) {
  const response = await PLivroAndamentoFinalizarData(id, data);

  return response;
}

export const PLivroAndamentoFinalizarService = withClientErrorHandler(
  executePLivroAndamentoFinalizarService,
);
