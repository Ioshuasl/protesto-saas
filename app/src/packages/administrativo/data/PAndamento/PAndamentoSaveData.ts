'use server';

import { PANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PAndamento/pAndamentoDataConfig';
import type {
  PAndamentoInterface,
  PAndamentoSavePayload,
  PAndamentoUpdatePayload,
} from '@/packages/administrativo/interfaces/PAndamento/PAndamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePAndamentoSaveCreateData(
  data: PAndamentoSavePayload,
): Promise<PAndamentoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: PANDAMENTO_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PAndamentoInterface;
  }

  throw new Error(response?.message ?? 'Erro ao cadastrar andamento');
}

async function executePAndamentoSaveUpdateData(
  id: number,
  data: PAndamentoUpdatePayload,
): Promise<PAndamentoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: PANDAMENTO_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PAndamentoInterface;
  }

  throw new Error(response?.message ?? 'Erro ao atualizar andamento');
}

export const PAndamentoSaveCreateData = withClientErrorHandler(executePAndamentoSaveCreateData);
export const PAndamentoSaveUpdateData = withClientErrorHandler(executePAndamentoSaveUpdateData);
