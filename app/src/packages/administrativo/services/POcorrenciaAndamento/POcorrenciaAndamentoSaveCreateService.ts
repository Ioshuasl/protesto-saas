'use server';

import { POcorrenciaAndamentoSaveCreateData } from '@/packages/administrativo/data/POcorrenciaAndamento/POcorrenciaAndamentoSaveData';
import type { POcorrenciaAndamentoSavePayload } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePOcorrenciaAndamentoSaveCreateService(
  data: POcorrenciaAndamentoSavePayload,
) {
  return await POcorrenciaAndamentoSaveCreateData(data);
}

export const POcorrenciaAndamentoSaveCreateService = withClientErrorHandler(
  executePOcorrenciaAndamentoSaveCreateService,
);
