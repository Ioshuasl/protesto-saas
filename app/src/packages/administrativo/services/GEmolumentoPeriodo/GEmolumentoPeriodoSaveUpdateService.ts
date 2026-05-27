'use server';

import { GEmolumentoPeriodoSaveUpdateData } from '@/packages/administrativo/data/GEmolumentoPeriodo/GEmolumentoPeriodoSaveData';
import type { GEmolumentoPeriodoInterface } from '@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoPeriodoSaveUpdateService(
  id: number,
  data: Partial<GEmolumentoPeriodoInterface>,
) {
  const response = await GEmolumentoPeriodoSaveUpdateData(id, data);

  return response;
}

export const GEmolumentoPeriodoSaveUpdateService = withClientErrorHandler(
  executeGEmolumentoPeriodoSaveUpdateService,
);
