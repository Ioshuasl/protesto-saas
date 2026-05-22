'use server';

import { POCORRENCIAS_ENDPOINTS } from '@/packages/administrativo/data/POcorrencias/pocorrenciasDataConfig';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePOcorrenciasDeleteData(id: number) {
  const api = new API();
  return await api.send({
    method: Methods.DELETE,
    endpoint: POCORRENCIAS_ENDPOINTS.delete(id),
  });
}

export const POcorrenciasDeleteData = withClientErrorHandler(executePOcorrenciasDeleteData);
