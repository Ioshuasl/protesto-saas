'use server';

import { PMOTIVOS_CANCELAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PMotivosCancelamento/pmotivosCancelamentoDataConfig';
import type { PMotivosCancelamentoInterface } from '@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePMotivosCancelamentoShowData(
  id: number,
): Promise<PMotivosCancelamentoInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: PMOTIVOS_CANCELAMENTO_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PMotivosCancelamentoInterface;
  }

  return undefined;
}

export const PMotivosCancelamentoShowData = withClientErrorHandler(
  executePMotivosCancelamentoShowData,
);
