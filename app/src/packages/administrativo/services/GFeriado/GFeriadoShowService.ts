'use server';

import { GFeriadoShowData } from '@/packages/administrativo/data/GFeriado/GFeriadoShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGFeriadoShowService(id: number) {
  const response = await GFeriadoShowData(id);

  return response;
}

export const GFeriadoShowService = withClientErrorHandler(executeGFeriadoShowService);
