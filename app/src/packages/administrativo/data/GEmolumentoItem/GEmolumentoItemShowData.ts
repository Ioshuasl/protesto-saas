'use server';

import { G_EMOLUMENTO_ITEM_ENDPOINTS } from '@/packages/administrativo/data/GEmolumentoItem/gEmolumentoItemDataConfig';
import type { GEmolumentoItemInterface } from '@/packages/administrativo/interfaces/GEmolumentoItem/GEmolumentoItemInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGEmolumentoItemShowData(id: number): Promise<GEmolumentoItemInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: G_EMOLUMENTO_ITEM_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GEmolumentoItemInterface;
  }

  return undefined;
}

export const GEmolumentoItemShowData = withClientErrorHandler(executeGEmolumentoItemShowData);
