'use server';

import { GSISTEMA_ENDPOINTS } from '@/packages/administrativo/data/GSistema/gsistemaDataConfig';
import type { GSistemaInterface } from '@/packages/administrativo/interfaces/GSistema/GSistemaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGSistemaSaveCreateData(
  data: GSistemaInterface,
): Promise<GSistemaInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: GSISTEMA_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GSistemaInterface;
  }

  throw new Error(
    typeof response?.message === 'string' ? response.message : 'Não foi possível salvar o sistema',
  );
}

async function executeGSistemaSaveUpdateData(
  id: number,
  data: Partial<Omit<GSistemaInterface, 'sistema_id'>>,
): Promise<GSistemaInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: GSISTEMA_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GSistemaInterface;
  }

  throw new Error(
    typeof response?.message === 'string'
      ? response.message
      : 'Não foi possível atualizar o sistema',
  );
}

export const GSistemaSaveCreateData = withClientErrorHandler(executeGSistemaSaveCreateData);
export const GSistemaSaveUpdateData = withClientErrorHandler(executeGSistemaSaveUpdateData);
