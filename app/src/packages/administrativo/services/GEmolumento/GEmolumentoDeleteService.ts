'use server';

import { GEmolumentoDeleteData } from '@/packages/administrativo/data/GEmolumento/GEmolumentoDeleteData';
import type { GEmolumentoInterface } from '@/packages/administrativo/interfaces/GEmolumento/GEmolumentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoDeleteService(data: GEmolumentoInterface) {
  const response = await GEmolumentoDeleteData(data);

  return response;
}

export const GEmolumentoDeleteService = withClientErrorHandler(executeGEmolumentoDeleteService);
