'use server';

import { POcorrenciaAndamentoDeleteData } from '@/packages/administrativo/data/POcorrenciaAndamento/POcorrenciaAndamentoDeleteData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePOcorrenciaAndamentoDeleteService(id: number) {
  return await POcorrenciaAndamentoDeleteData(id);
}

export const POcorrenciaAndamentoDeleteService = withClientErrorHandler(
  executePOcorrenciaAndamentoDeleteService,
);
