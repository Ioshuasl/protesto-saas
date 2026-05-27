'use server';

import { GEmolumentoItemUpdateData } from '@/packages/administrativo/data/GEmolumentoItem/GEmolumentoItemUpdateData';
import type { GEmolumentoItemInterface } from '@/packages/administrativo/interfaces/GEmolumentoItem/GEmolumentoItemInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoItemUpdateService(
  id: number,
  data: Partial<GEmolumentoItemInterface>,
) {
  const response = await GEmolumentoItemUpdateData(id, data);

  return response;
}

export const GEmolumentoItemUpdateService = withClientErrorHandler(executeGEmolumentoItemUpdateService);
