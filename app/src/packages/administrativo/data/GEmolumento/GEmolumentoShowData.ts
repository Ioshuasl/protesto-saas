'use server';

import { GEMOLUMENTO_ENDPOINTS } from '@/packages/administrativo/data/GEmolumento/gemolumentoDataConfig';
import type { GEmolumentoInterface } from '@/packages/administrativo/interfaces/GEmolumento/GEmolumentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGEmolumentoShowData(id: number): Promise<GEmolumentoInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: GEMOLUMENTO_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GEmolumentoInterface;
  }

  return undefined;
}

export const GEmolumentoShowData = withClientErrorHandler(executeGEmolumentoShowData);
