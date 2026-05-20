'use server';

import { PMotivosIndexData } from '@/packages/administrativo/data/PMotivos/PMotivosIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosIndexService() {
  const response = await PMotivosIndexData();

  return response;
}

export const PMotivosIndexService = withClientErrorHandler(executePMotivosIndexService);
