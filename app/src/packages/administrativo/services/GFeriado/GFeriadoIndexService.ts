'use server';

import { GFeriadoIndexData } from '@/packages/administrativo/data/GFeriado/GFeriadoIndexData';
import type { GFeriadoIndexQuery } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGFeriadoIndexService(query?: GFeriadoIndexQuery) {
  const response = await GFeriadoIndexData(query);

  return response;
}

export const GFeriadoIndexService = withClientErrorHandler(executeGFeriadoIndexService);
