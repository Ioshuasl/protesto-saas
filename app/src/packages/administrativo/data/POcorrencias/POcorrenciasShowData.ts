'use server';

import { POCORRENCIAS_ENDPOINTS } from '@/packages/administrativo/data/POcorrencias/pocorrenciasDataConfig';
import type { POcorrenciasInterface } from '@/packages/administrativo/interfaces/POcorrencias/POcorrenciasInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePOcorrenciasShowData(
  id: number,
): Promise<POcorrenciasInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: POCORRENCIAS_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as POcorrenciasInterface;
  }

  return undefined;
}

export const POcorrenciasShowData = withClientErrorHandler(executePOcorrenciasShowData);
