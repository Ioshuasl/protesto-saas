'use server';

import { GFeriadoIndexData } from '@/packages/administrativo/data/GFeriado/GFeriadoIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGFeriadoIndexService() {
  const response = await GFeriadoIndexData();

  return response;
}

export const GFeriadoIndexService = withClientErrorHandler(executeGFeriadoIndexService);
