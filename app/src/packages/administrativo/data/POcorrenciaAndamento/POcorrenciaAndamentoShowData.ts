'use server';

import { POCORRENCIA_ANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/POcorrenciaAndamento/pocorrenciaAndamentoDataConfig';
import type { POcorrenciaAndamentoInterface } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePOcorrenciaAndamentoShowData(
  id: number,
): Promise<POcorrenciaAndamentoInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: POCORRENCIA_ANDAMENTO_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as POcorrenciaAndamentoInterface;
  }

  return undefined;
}

export const POcorrenciaAndamentoShowData = withClientErrorHandler(
  executePOcorrenciaAndamentoShowData,
);
