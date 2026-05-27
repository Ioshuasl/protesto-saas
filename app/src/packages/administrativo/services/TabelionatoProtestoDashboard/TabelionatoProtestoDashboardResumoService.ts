'use server';

import { TabelionatoProtestoDashboardResumoData } from '@/packages/administrativo/data/TabelionatoProtestoDashboard/TabelionatoProtestoDashboardResumoData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeTabelionatoProtestoDashboardResumoService() {
  return await TabelionatoProtestoDashboardResumoData();
}

export const TabelionatoProtestoDashboardResumoService = withClientErrorHandler(
  executeTabelionatoProtestoDashboardResumoService,
);
