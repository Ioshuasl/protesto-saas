'use server';

import { G_EMOLUMENTO_ITEM_ENDPOINTS } from '@/packages/administrativo/data/GEmolumentoItem/gEmolumentoItemDataConfig';
import type { GEmolumentoItemInterface } from '@/packages/administrativo/interfaces/GEmolumentoItem/GEmolumentoItemInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGEmolumentoItemUpdateData(
  id: number,
  data: Partial<GEmolumentoItemInterface>,
): Promise<GEmolumentoItemInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: G_EMOLUMENTO_ITEM_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GEmolumentoItemInterface;
  }

  throw new Error(
    typeof response?.message === 'string'
      ? response.message
      : 'Nao foi possivel atualizar o item de emolumento',
  );
}

export const GEmolumentoItemUpdateData = withClientErrorHandler(executeGEmolumentoItemUpdateData);
