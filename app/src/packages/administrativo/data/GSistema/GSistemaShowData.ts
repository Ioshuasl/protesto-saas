'use server';

import { GSISTEMA_ENDPOINTS } from '@/packages/administrativo/data/GSistema/gsistemaDataConfig';
import type { GSistemaInterface } from '@/packages/administrativo/interfaces/GSistema/GSistemaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGSistemaShowData(id: number): Promise<GSistemaInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: GSISTEMA_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GSistemaInterface;
  }

  return undefined;
}

export const GSistemaShowData = withClientErrorHandler(executeGSistemaShowData);
