'use server';

import { POcorrenciasIndexData } from '@/packages/administrativo/data/POcorrencias/POcorrenciasIndexData';
import type { POcorrenciasIndexQuery } from '@/packages/administrativo/interfaces/POcorrencias/POcorrenciasIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePOcorrenciasIndexService(query?: POcorrenciasIndexQuery) {
  const response = await POcorrenciasIndexData(query);

  return response;
}

export const POcorrenciasIndexService = withClientErrorHandler(executePOcorrenciasIndexService);
