'use server';

import { POcorrenciasIndexData } from '@/packages/administrativo/data/POcorrencias/POcorrenciasIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePOcorrenciasIndexService() {
  const response = await POcorrenciasIndexData();

  return response;
}

export const POcorrenciasIndexService = withClientErrorHandler(executePOcorrenciasIndexService);
