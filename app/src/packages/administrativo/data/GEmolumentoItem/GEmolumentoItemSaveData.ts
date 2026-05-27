'use server';

import { G_EMOLUMENTO_ITEM_ENDPOINTS } from '@/packages/administrativo/data/GEmolumentoItem/gEmolumentoItemDataConfig';
import type { GEmolumentoItemInterface } from '@/packages/administrativo/interfaces/GEmolumentoItem/GEmolumentoItemInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGEmolumentoItemSaveData(
  data: Omit<GEmolumentoItemInterface, 'emolumento_item_id'>,
): Promise<GEmolumentoItemInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: G_EMOLUMENTO_ITEM_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GEmolumentoItemInterface;
  }

  throw new Error(
    typeof response?.message === 'string'
      ? response.message
      : 'Nao foi possivel salvar o item de emolumento',
  );
}

export const GEmolumentoItemSaveData = withClientErrorHandler(executeGEmolumentoItemSaveData);
