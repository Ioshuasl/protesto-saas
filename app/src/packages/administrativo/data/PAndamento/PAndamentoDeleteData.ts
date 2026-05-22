'use server';

import { PANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PAndamento/pAndamentoDataConfig';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePAndamentoDeleteData(id: number) {
  const api = new API();
  return await api.send({
    method: Methods.DELETE,
    endpoint: PANDAMENTO_ENDPOINTS.delete(id),
  });
}

export const PAndamentoDeleteData = withClientErrorHandler(executePAndamentoDeleteData);
