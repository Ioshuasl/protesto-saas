'use server';

import { GEmolumentoPeriodoSaveCreateData } from '@/packages/administrativo/data/GEmolumentoPeriodo/GEmolumentoPeriodoSaveData';
import type { GEmolumentoPeriodoInterface } from '@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoPeriodoSaveCreateService(
  data: Omit<GEmolumentoPeriodoInterface, 'emolumento_periodo_id'>,
) {
  const response = await GEmolumentoPeriodoSaveCreateData(data);

  return response;
}

export const GEmolumentoPeriodoSaveCreateService = withClientErrorHandler(
  executeGEmolumentoPeriodoSaveCreateService,
);
