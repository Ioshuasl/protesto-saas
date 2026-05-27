'use server';

import { TABELIONATO_PROTESTO_DASHBOARD_ENDPOINTS } from '@/packages/administrativo/data/TabelionatoProtestoDashboard/tabelionatoProtestoDashboardDataConfig';
import type { TabelionatoProtestoDashboardFunilItem } from '@/packages/administrativo/interfaces/TabelionatoProtestoDashboard/TabelionatoProtestoDashboardFunilItem';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeTabelionatoProtestoDashboardFunilData(): Promise<TabelionatoProtestoDashboardFunilItem[]> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: TABELIONATO_PROTESTO_DASHBOARD_ENDPOINTS.funil,
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return [];
  }

  return Array.isArray(response?.data) ? (response.data as TabelionatoProtestoDashboardFunilItem[]) : [];
}

export const TabelionatoProtestoDashboardFunilData = withClientErrorHandler(
  executeTabelionatoProtestoDashboardFunilData,
);
