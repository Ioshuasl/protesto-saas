'use server';

import { G_EMOLUMENTO_PERIODO_ENDPOINTS } from '@/packages/administrativo/data/GEmolumentoPeriodo/gEmolumentoPeriodoDataConfig';
import type { GEmolumentoPeriodoInterface } from '@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGEmolumentoPeriodoSaveCreateData(
  data: Omit<GEmolumentoPeriodoInterface, 'emolumento_periodo_id'>,
): Promise<GEmolumentoPeriodoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: G_EMOLUMENTO_PERIODO_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GEmolumentoPeriodoInterface;
  }

  throw new Error(
    typeof response?.message === 'string'
      ? response.message
      : 'Nao foi possivel criar o periodo de emolumento',
  );
}

async function executeGEmolumentoPeriodoSaveUpdateData(
  id: number,
  data: Partial<GEmolumentoPeriodoInterface>,
): Promise<GEmolumentoPeriodoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: G_EMOLUMENTO_PERIODO_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GEmolumentoPeriodoInterface;
  }

  throw new Error(
    typeof response?.message === 'string'
      ? response.message
      : 'Nao foi possivel atualizar o periodo de emolumento',
  );
}

export const GEmolumentoPeriodoSaveCreateData = withClientErrorHandler(
  executeGEmolumentoPeriodoSaveCreateData,
);
export const GEmolumentoPeriodoSaveUpdateData = withClientErrorHandler(
  executeGEmolumentoPeriodoSaveUpdateData,
);
