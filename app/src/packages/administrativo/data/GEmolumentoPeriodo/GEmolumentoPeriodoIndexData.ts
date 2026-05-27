'use server';

import { G_EMOLUMENTO_PERIODO_ENDPOINTS } from '@/packages/administrativo/data/GEmolumentoPeriodo/gEmolumentoPeriodoDataConfig';
import type { GEmolumentoPeriodoInterface } from '@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGEmolumentoPeriodoIndexData(): Promise<GEmolumentoPeriodoInterface[]> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: G_EMOLUMENTO_PERIODO_ENDPOINTS.index,
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return [];
  }

  return Array.isArray(response?.data) ? (response.data as GEmolumentoPeriodoInterface[]) : [];
}

export const GEmolumentoPeriodoIndexData = withClientErrorHandler(executeGEmolumentoPeriodoIndexData);
