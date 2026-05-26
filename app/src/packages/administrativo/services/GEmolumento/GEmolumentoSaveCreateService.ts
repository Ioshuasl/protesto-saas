'use server';

import { GEmolumentoSaveCreateData } from '@/packages/administrativo/data/GEmolumento/GEmolumentoSaveData';
import type { GEmolumentoInterface } from '@/packages/administrativo/interfaces/GEmolumento/GEmolumentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoSaveCreateService(
  data: Omit<GEmolumentoInterface, 'emolumento_id'>,
) {
  const response = await GEmolumentoSaveCreateData(data);

  return response;
}

export const GEmolumentoSaveCreateService = withClientErrorHandler(
  executeGEmolumentoSaveCreateService,
);
