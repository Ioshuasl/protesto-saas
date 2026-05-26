'use server';

import { GEmolumentoIndexData } from '@/packages/administrativo/data/GEmolumento/GEmolumentoIndexData';
import type { GEmolumentoIndexQuery } from '@/packages/administrativo/interfaces/GEmolumento/GEmolumentoIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoIndexService(
  sistemaId: number,
  query?: GEmolumentoIndexQuery,
) {
  const response = await GEmolumentoIndexData(sistemaId, query);

  return response;
}

export const GEmolumentoIndexService = withClientErrorHandler(executeGEmolumentoIndexService);
