'use server';

import { PMotivosIndexData } from '@/packages/administrativo/data/PMotivos/PMotivosIndexData';
import type { PMotivosIndexQuery } from '@/packages/administrativo/interfaces/PMotivos/PMotivosIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosIndexService(query?: PMotivosIndexQuery) {
  const response = await PMotivosIndexData(query);

  return response;
}

export const PMotivosIndexService = withClientErrorHandler(executePMotivosIndexService);
