'use server';

import { PBANCO_ENDPOINTS } from '@/packages/administrativo/data/PBanco/pbancoDataConfig';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePBancoDeleteData(id: number) {
  const api = new API();
  return await api.send({
    method: Methods.DELETE,
    endpoint: PBANCO_ENDPOINTS.delete(id),
  });
}

export const PBancoDeleteData = withClientErrorHandler(executePBancoDeleteData);
