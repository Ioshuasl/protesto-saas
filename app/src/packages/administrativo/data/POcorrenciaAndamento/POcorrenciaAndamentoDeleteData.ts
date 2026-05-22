'use server';

import { POCORRENCIA_ANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/POcorrenciaAndamento/pocorrenciaAndamentoDataConfig';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePOcorrenciaAndamentoDeleteData(id: number) {
  const api = new API();
  return await api.send({
    method: Methods.DELETE,
    endpoint: POCORRENCIA_ANDAMENTO_ENDPOINTS.delete(id),
  });
}

export const POcorrenciaAndamentoDeleteData = withClientErrorHandler(
  executePOcorrenciaAndamentoDeleteData,
);
