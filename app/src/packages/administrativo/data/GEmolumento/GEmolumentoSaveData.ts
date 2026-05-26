'use server';

import { GEMOLUMENTO_ENDPOINTS } from '@/packages/administrativo/data/GEmolumento/gemolumentoDataConfig';
import type { GEmolumentoInterface } from '@/packages/administrativo/interfaces/GEmolumento/GEmolumentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGEmolumentoSaveCreateData(
  data: Omit<GEmolumentoInterface, 'emolumento_id'>,
): Promise<GEmolumentoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: GEMOLUMENTO_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GEmolumentoInterface;
  }

  throw new Error(
    typeof response?.message === 'string' ? response.message : 'Não foi possível salvar o emolumento',
  );
}

async function executeGEmolumentoSaveUpdateData(
  id: number,
  data: Partial<GEmolumentoInterface>,
): Promise<GEmolumentoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: GEMOLUMENTO_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GEmolumentoInterface;
  }

  throw new Error(
    typeof response?.message === 'string'
      ? response.message
      : 'Não foi possível atualizar o emolumento',
  );
}

export const GEmolumentoSaveCreateData = withClientErrorHandler(
  executeGEmolumentoSaveCreateData,
);
export const GEmolumentoSaveUpdateData = withClientErrorHandler(
  executeGEmolumentoSaveUpdateData,
);
