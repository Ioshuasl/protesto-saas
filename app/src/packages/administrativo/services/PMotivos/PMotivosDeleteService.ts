'use server';

import { PMotivosDeleteData } from '@/packages/administrativo/data/PMotivos/PMotivosDeleteData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosDeleteService(id: number) {
  const response = await PMotivosDeleteData(id);

  return response;
}

export const PMotivosDeleteService = withClientErrorHandler(executePMotivosDeleteService);
