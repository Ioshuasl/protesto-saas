'use server';

import { GFeriadoSaveCreateData } from '@/packages/administrativo/data/GFeriado/GFeriadoSaveData';
import type { GFeriadoInterface } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGFeriadoSaveCreateService(data: Omit<GFeriadoInterface, 'feriado_id'>) {
  const response = await GFeriadoSaveCreateData(data);

  return response;
}

export const GFeriadoSaveCreateService = withClientErrorHandler(executeGFeriadoSaveCreateService);
