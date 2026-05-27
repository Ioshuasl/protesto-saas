'use server';

import { GEmolumentoListData } from '@/packages/administrativo/data/GEmolumentoList/GEmolumentoListData';
import type { GEmolumentoListQuery } from '@/packages/administrativo/interfaces/GEmolumentoList/GEmolumentoListInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoListService(query?: GEmolumentoListQuery) {
  const response = await GEmolumentoListData(query);
  return response;
}

export const GEmolumentoListService = withClientErrorHandler(executeGEmolumentoListService);
