'use server';

import { G_EMOLUMENTO_ITEM_ENDPOINTS } from '@/packages/administrativo/data/GEmolumentoItem/gEmolumentoItemDataConfig';
import type { GEmolumentoItemInterface } from '@/packages/administrativo/interfaces/GEmolumentoItem/GEmolumentoItemInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGEmolumentoItemIndexData(
  emolumentoId: number,
  emolumentoPeriodoId: number,
): Promise<GEmolumentoItemInterface[]> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: G_EMOLUMENTO_ITEM_ENDPOINTS.index(emolumentoId, emolumentoPeriodoId),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return [];
  }

  return Array.isArray(response?.data) ? (response.data as GEmolumentoItemInterface[]) : [];
}

export const GEmolumentoItemIndexData = withClientErrorHandler(executeGEmolumentoItemIndexData);
