'use server';

import { PMOTIVOS_ENDPOINTS } from '@/packages/administrativo/data/PMotivos/pmotivosDataConfig';
import type { PMotivosInterface } from '@/packages/administrativo/interfaces/PMotivos/PMotivosInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePMotivosSaveCreateData(
  data: Omit<PMotivosInterface, 'motivos_id'>,
): Promise<PMotivosInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: PMOTIVOS_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PMotivosInterface;
  }

  throw new Error(response?.message ?? 'Erro ao cadastrar motivo de apontamento');
}

async function executePMotivosSaveUpdateData(
  id: number,
  data: Partial<PMotivosInterface>,
): Promise<PMotivosInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: PMOTIVOS_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PMotivosInterface;
  }

  throw new Error(response?.message ?? 'Erro ao atualizar motivo de apontamento');
}

export const PMotivosSaveCreateData = withClientErrorHandler(executePMotivosSaveCreateData);
export const PMotivosSaveUpdateData = withClientErrorHandler(executePMotivosSaveUpdateData);
