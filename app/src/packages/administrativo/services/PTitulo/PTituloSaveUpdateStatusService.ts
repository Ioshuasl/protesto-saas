'use server';

import { PTituloSaveUpdateStatusData } from '@/packages/administrativo/data/PTitulo/PTituloSaveData';
import type { TituloStatus } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloSaveUpdateStatusService(id: number, status: TituloStatus) {
  const response = await PTituloSaveUpdateStatusData(id, status);

  return response;
}

export const PTituloSaveUpdateStatusService = withClientErrorHandler(
  executePTituloSaveUpdateStatusService,
);
