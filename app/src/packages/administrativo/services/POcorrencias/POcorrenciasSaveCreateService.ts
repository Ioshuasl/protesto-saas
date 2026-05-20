'use server';

import { POcorrenciasSaveCreateData } from '@/packages/administrativo/data/POcorrencias/POcorrenciasSaveData';
import type { POcorrenciasInterface } from '@/packages/administrativo/interfaces/POcorrencias/POcorrenciasInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePOcorrenciasSaveCreateService(
  data: Omit<POcorrenciasInterface, 'ocorrencias_id'>,
) {
  const response = await POcorrenciasSaveCreateData(data);

  return response;
}

export const POcorrenciasSaveCreateService = withClientErrorHandler(
  executePOcorrenciasSaveCreateService,
);
