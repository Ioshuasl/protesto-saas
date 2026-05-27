'use server';

import { G_EMOLUMENTO_PERIODO_ENDPOINTS } from '@/packages/administrativo/data/GEmolumentoPeriodo/gEmolumentoPeriodoDataConfig';
import type { GEmolumentoPeriodoInterface } from '@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGEmolumentoPeriodoShowData(
  id: number,
): Promise<GEmolumentoPeriodoInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: G_EMOLUMENTO_PERIODO_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GEmolumentoPeriodoInterface;
  }

  return undefined;
}

export const GEmolumentoPeriodoShowData = withClientErrorHandler(executeGEmolumentoPeriodoShowData);
