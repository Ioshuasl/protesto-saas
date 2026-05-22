'use server';

import { POcorrenciaAndamentoSaveUpdateData } from '@/packages/administrativo/data/POcorrenciaAndamento/POcorrenciaAndamentoSaveData';
import type { POcorrenciaAndamentoSavePayload } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePOcorrenciaAndamentoSaveUpdateService(
  id: number,
  data: Partial<POcorrenciaAndamentoSavePayload>,
) {
  return await POcorrenciaAndamentoSaveUpdateData(id, data);
}

export const POcorrenciaAndamentoSaveUpdateService = withClientErrorHandler(
  executePOcorrenciaAndamentoSaveUpdateService,
);
