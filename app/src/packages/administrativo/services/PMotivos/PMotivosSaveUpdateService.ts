'use server';

import { PMotivosSaveUpdateData } from '@/packages/administrativo/data/PMotivos/PMotivosSaveData';
import type { PMotivosInterface } from '@/packages/administrativo/interfaces/PMotivos/PMotivosInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosSaveUpdateService(id: number, data: Partial<PMotivosInterface>) {
  const response = await PMotivosSaveUpdateData(id, data);

  return response;
}

export const PMotivosSaveUpdateService = withClientErrorHandler(executePMotivosSaveUpdateService);
