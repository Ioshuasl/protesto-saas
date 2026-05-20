'use server';

import { POcorrenciasDeleteData } from '@/packages/administrativo/data/POcorrencias/POcorrenciasDeleteData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePOcorrenciasDeleteService(id: number) {
  const response = await POcorrenciasDeleteData(id);

  return response;
}

export const POcorrenciasDeleteService = withClientErrorHandler(executePOcorrenciasDeleteService);
