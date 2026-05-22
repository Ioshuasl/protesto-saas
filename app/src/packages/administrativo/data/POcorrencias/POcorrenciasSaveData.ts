'use server';

import { POCORRENCIAS_ENDPOINTS } from '@/packages/administrativo/data/POcorrencias/pocorrenciasDataConfig';
import type { POcorrenciasInterface } from '@/packages/administrativo/interfaces/POcorrencias/POcorrenciasInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePOcorrenciasSaveCreateData(
  data: Omit<POcorrenciasInterface, 'ocorrencias_id'>,
): Promise<POcorrenciasInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: POCORRENCIAS_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as POcorrenciasInterface;
  }

  throw new Error(response?.message ?? 'Erro ao cadastrar ocorrência');
}

async function executePOcorrenciasSaveUpdateData(
  id: number,
  data: Partial<POcorrenciasInterface>,
): Promise<POcorrenciasInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: POCORRENCIAS_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as POcorrenciasInterface;
  }

  throw new Error(response?.message ?? 'Erro ao atualizar ocorrência');
}

export const POcorrenciasSaveCreateData = withClientErrorHandler(executePOcorrenciasSaveCreateData);
export const POcorrenciasSaveUpdateData = withClientErrorHandler(executePOcorrenciasSaveUpdateData);
