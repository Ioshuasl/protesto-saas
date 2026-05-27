'use server';

import { GEmolumentoPeriodoShowData } from '@/packages/administrativo/data/GEmolumentoPeriodo/GEmolumentoPeriodoShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoPeriodoShowService(id: number) {
  const response = await GEmolumentoPeriodoShowData(id);

  return response;
}

export const GEmolumentoPeriodoShowService = withClientErrorHandler(
  executeGEmolumentoPeriodoShowService,
);
