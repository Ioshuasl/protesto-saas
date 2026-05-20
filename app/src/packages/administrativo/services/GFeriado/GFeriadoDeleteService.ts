'use server';

import { GFeriadoDeleteData } from '@/packages/administrativo/data/GFeriado/GFeriadoDeleteData';
import { GFeriadoInterface } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGFeriadoDeleteService(data: GFeriadoInterface) {
  const response = await GFeriadoDeleteData(data);

  return response;
}

export const GFeriadoDeleteService = withClientErrorHandler(executeGFeriadoDeleteService);
