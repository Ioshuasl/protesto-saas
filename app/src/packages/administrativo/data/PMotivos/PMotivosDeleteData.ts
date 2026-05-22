'use server';

import { PMOTIVOS_ENDPOINTS } from '@/packages/administrativo/data/PMotivos/pmotivosDataConfig';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePMotivosDeleteData(id: number) {
  const api = new API();
  return await api.send({
    method: Methods.DELETE,
    endpoint: PMOTIVOS_ENDPOINTS.delete(id),
  });
}

export const PMotivosDeleteData = withClientErrorHandler(executePMotivosDeleteData);
