'use server';

import { POCORRENCIA_ANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/POcorrenciaAndamento/pocorrenciaAndamentoDataConfig';
import type { POcorrenciaAndamentoInterface } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface';
import type { POcorrenciaAndamentoSavePayload } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePOcorrenciaAndamentoSaveCreateData(
  data: POcorrenciaAndamentoSavePayload,
): Promise<POcorrenciaAndamentoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: POCORRENCIA_ANDAMENTO_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as POcorrenciaAndamentoInterface;
  }

  throw new Error(response?.message ?? 'Erro ao cadastrar ocorrência de andamento');
}

async function executePOcorrenciaAndamentoSaveUpdateData(
  id: number,
  data: Partial<POcorrenciaAndamentoSavePayload>,
): Promise<POcorrenciaAndamentoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: POCORRENCIA_ANDAMENTO_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as POcorrenciaAndamentoInterface;
  }

  throw new Error(response?.message ?? 'Erro ao atualizar ocorrência de andamento');
}

export const POcorrenciaAndamentoSaveCreateData = withClientErrorHandler(
  executePOcorrenciaAndamentoSaveCreateData,
);
export const POcorrenciaAndamentoSaveUpdateData = withClientErrorHandler(
  executePOcorrenciaAndamentoSaveUpdateData,
);
