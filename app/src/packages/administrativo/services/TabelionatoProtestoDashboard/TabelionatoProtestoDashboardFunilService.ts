'use server';

import { TabelionatoProtestoDashboardFunilData } from '@/packages/administrativo/data/TabelionatoProtestoDashboard/TabelionatoProtestoDashboardFunilData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeTabelionatoProtestoDashboardFunilService() {
  return await TabelionatoProtestoDashboardFunilData();
}

export const TabelionatoProtestoDashboardFunilService = withClientErrorHandler(
  executeTabelionatoProtestoDashboardFunilService,
);
