'use server';

import { PMotivosSaveCreateData } from '@/packages/administrativo/data/PMotivos/PMotivosSaveData';
import type { PMotivosInterface } from '@/packages/administrativo/interfaces/PMotivos/PMotivosInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosSaveCreateService(data: Omit<PMotivosInterface, 'motivos_id'>) {
  const response = await PMotivosSaveCreateData(data);

  return response;
}

export const PMotivosSaveCreateService = withClientErrorHandler(executePMotivosSaveCreateService);
