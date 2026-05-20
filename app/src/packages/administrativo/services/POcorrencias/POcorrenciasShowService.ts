'use server';

import { POcorrenciasShowData } from '@/packages/administrativo/data/POcorrencias/POcorrenciasShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePOcorrenciasShowService(id: number) {
  const response = await POcorrenciasShowData(id);

  return response;
}

export const POcorrenciasShowService = withClientErrorHandler(executePOcorrenciasShowService);
