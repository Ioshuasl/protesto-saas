'use server';

import { GEMOLUMENTO_ENDPOINTS } from '@/packages/administrativo/data/GEmolumento/gemolumentoDataConfig';
import type { GEmolumentoInterface } from '@/packages/administrativo/interfaces/GEmolumento/GEmolumentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGEmolumentoDeleteData(data: GEmolumentoInterface) {
  const api = new API();
  return api.send({
    method: Methods.DELETE,
    endpoint: GEMOLUMENTO_ENDPOINTS.delete(data.emolumento_id),
  });
}

export const GEmolumentoDeleteData = withClientErrorHandler(executeGEmolumentoDeleteData);
