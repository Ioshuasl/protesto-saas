'use server';

import { PMOTIVOS_CANCELAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PMotivosCancelamento/pmotivosCancelamentoDataConfig';
import type { PMotivosCancelamentoInterface } from '@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export type PMotivosCancelamentoSavePayload = {
  descricao: string;
  situacao: string;
};

async function executePMotivosCancelamentoSaveCreateData(
  data: PMotivosCancelamentoSavePayload,
): Promise<PMotivosCancelamentoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: PMOTIVOS_CANCELAMENTO_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PMotivosCancelamentoInterface;
  }

  throw new Error(response?.message ?? 'Erro ao cadastrar motivo de cancelamento');
}

async function executePMotivosCancelamentoSaveUpdateData(
  id: number,
  data: Partial<PMotivosCancelamentoSavePayload>,
): Promise<PMotivosCancelamentoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: PMOTIVOS_CANCELAMENTO_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PMotivosCancelamentoInterface;
  }

  throw new Error(response?.message ?? 'Erro ao atualizar motivo de cancelamento');
}

export const PMotivosCancelamentoSaveCreateData = withClientErrorHandler(
  executePMotivosCancelamentoSaveCreateData,
);
export const PMotivosCancelamentoSaveUpdateData = withClientErrorHandler(
  executePMotivosCancelamentoSaveUpdateData,
);
