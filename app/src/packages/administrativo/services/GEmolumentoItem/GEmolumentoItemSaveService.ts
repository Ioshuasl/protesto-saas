'use server';

import { GEmolumentoItemSaveData } from '@/packages/administrativo/data/GEmolumentoItem/GEmolumentoItemSaveData';
import type { GEmolumentoItemInterface } from '@/packages/administrativo/interfaces/GEmolumentoItem/GEmolumentoItemInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoItemSaveService(
  data: Omit<GEmolumentoItemInterface, 'emolumento_item_id'>,
) {
  const response = await GEmolumentoItemSaveData(data);

  return response;
}

export const GEmolumentoItemSaveService = withClientErrorHandler(executeGEmolumentoItemSaveService);
