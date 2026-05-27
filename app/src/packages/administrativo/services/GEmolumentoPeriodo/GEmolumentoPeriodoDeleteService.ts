'use server';

import { GEmolumentoPeriodoDeleteData } from '@/packages/administrativo/data/GEmolumentoPeriodo/GEmolumentoPeriodoDeleteData';
import type { GEmolumentoPeriodoInterface } from '@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoPeriodoDeleteService(data: GEmolumentoPeriodoInterface) {
  const response = await GEmolumentoPeriodoDeleteData(data);

  return response;
}

export const GEmolumentoPeriodoDeleteService = withClientErrorHandler(
  executeGEmolumentoPeriodoDeleteService,
);
