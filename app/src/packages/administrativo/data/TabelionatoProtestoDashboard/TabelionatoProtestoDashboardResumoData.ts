'use server';

import { TABELIONATO_PROTESTO_DASHBOARD_ENDPOINTS } from '@/packages/administrativo/data/TabelionatoProtestoDashboard/tabelionatoProtestoDashboardDataConfig';
import type { TabelionatoProtestoDashboardResumo } from '@/packages/administrativo/interfaces/TabelionatoProtestoDashboard/TabelionatoProtestoDashboardResumo';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeTabelionatoProtestoDashboardResumoData(): Promise<TabelionatoProtestoDashboardResumo | null> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: TABELIONATO_PROTESTO_DASHBOARD_ENDPOINTS.resumo,
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return null;
  }

  return (response?.data as TabelionatoProtestoDashboardResumo | undefined) ?? null;
}

export const TabelionatoProtestoDashboardResumoData = withClientErrorHandler(
  executeTabelionatoProtestoDashboardResumoData,
);
