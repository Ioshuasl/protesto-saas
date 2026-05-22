'use server';

import { PMOTIVOS_CANCELAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PMotivosCancelamento/pmotivosCancelamentoDataConfig';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePMotivosCancelamentoDeleteData(id: number) {
  const api = new API();
  return await api.send({
    method: Methods.DELETE,
    endpoint: PMOTIVOS_CANCELAMENTO_ENDPOINTS.delete(id),
  });
}

export const PMotivosCancelamentoDeleteData = withClientErrorHandler(
  executePMotivosCancelamentoDeleteData,
);
