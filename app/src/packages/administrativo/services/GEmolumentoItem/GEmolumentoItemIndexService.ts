'use server';

import { GEmolumentoItemIndexData } from '@/packages/administrativo/data/GEmolumentoItem/GEmolumentoItemIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoItemIndexService(emolumentoId: number, emolumentoPeriodoId: number) {
  const response = await GEmolumentoItemIndexData(emolumentoId, emolumentoPeriodoId);

  return response;
}

export const GEmolumentoItemIndexService = withClientErrorHandler(executeGEmolumentoItemIndexService);
