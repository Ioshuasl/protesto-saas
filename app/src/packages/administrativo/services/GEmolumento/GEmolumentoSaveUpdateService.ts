'use server';

import { GEmolumentoSaveUpdateData } from '@/packages/administrativo/data/GEmolumento/GEmolumentoSaveData';
import type { GEmolumentoInterface } from '@/packages/administrativo/interfaces/GEmolumento/GEmolumentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoSaveUpdateService(
  id: number,
  data: Partial<GEmolumentoInterface>,
) {
  const response = await GEmolumentoSaveUpdateData(id, data);

  return response;
}

export const GEmolumentoSaveUpdateService = withClientErrorHandler(
  executeGEmolumentoSaveUpdateService,
);
