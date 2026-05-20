'use server';

import { GFeriadoSaveUpdateData } from '@/packages/administrativo/data/GFeriado/GFeriadoSaveData';
import type { GFeriadoInterface } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGFeriadoSaveUpdateService(id: number, data: Partial<GFeriadoInterface>) {
  const response = await GFeriadoSaveUpdateData(id, data);

  return response;
}

export const GFeriadoSaveUpdateService = withClientErrorHandler(executeGFeriadoSaveUpdateService);
