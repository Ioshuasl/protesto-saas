'use server';

import { GFERIADO_ENDPOINTS } from '@/packages/administrativo/data/GFeriado/gferiadoDataConfig';
import type { GFeriadoInterface } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGFeriadoShowData(id: number): Promise<GFeriadoInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: GFERIADO_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GFeriadoInterface;
  }

  return undefined;
}

export const GFeriadoShowData = withClientErrorHandler(executeGFeriadoShowData);
