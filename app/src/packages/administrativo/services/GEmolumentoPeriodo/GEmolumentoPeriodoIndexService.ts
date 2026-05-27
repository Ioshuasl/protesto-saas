'use server';

import { GEmolumentoPeriodoIndexData } from '@/packages/administrativo/data/GEmolumentoPeriodo/GEmolumentoPeriodoIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoPeriodoIndexService() {
  const response = await GEmolumentoPeriodoIndexData();

  return response;
}

export const GEmolumentoPeriodoIndexService = withClientErrorHandler(
  executeGEmolumentoPeriodoIndexService,
);
