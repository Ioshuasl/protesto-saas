'use server';

import { POcorrenciasSaveUpdateData } from '@/packages/administrativo/data/POcorrencias/POcorrenciasSaveData';
import type { POcorrenciasInterface } from '@/packages/administrativo/interfaces/POcorrencias/POcorrenciasInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePOcorrenciasSaveUpdateService(
  id: number,
  data: Partial<POcorrenciasInterface>,
) {
  const response = await POcorrenciasSaveUpdateData(id, data);

  return response;
}

export const POcorrenciasSaveUpdateService = withClientErrorHandler(
  executePOcorrenciasSaveUpdateService,
);
