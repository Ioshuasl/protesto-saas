'use server';

import { PBANCO_ENDPOINTS } from '@/packages/administrativo/data/PBanco/pbancoDataConfig';
import type { PBancoInterface } from '@/packages/administrativo/interfaces/PBanco/PBancoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePBancoSaveCreateData(
  data: Omit<PBancoInterface, 'banco_id'>,
): Promise<PBancoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: PBANCO_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PBancoInterface;
  }

  throw new Error(response?.message ?? 'Erro ao cadastrar banco');
}

async function executePBancoSaveUpdateData(
  id: number,
  data: Partial<PBancoInterface>,
): Promise<PBancoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: PBANCO_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PBancoInterface;
  }

  throw new Error(response?.message ?? 'Erro ao atualizar banco');
}

export const PBancoSaveCreateData = withClientErrorHandler(executePBancoSaveCreateData);
export const PBancoSaveUpdateData = withClientErrorHandler(executePBancoSaveUpdateData);
