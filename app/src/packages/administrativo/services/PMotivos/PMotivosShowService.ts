'use server';

import { PMotivosShowData } from '@/packages/administrativo/data/PMotivos/PMotivosShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosShowService(id: number) {
  const response = await PMotivosShowData(id);

  return response;
}

export const PMotivosShowService = withClientErrorHandler(executePMotivosShowService);
