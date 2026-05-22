'use server';

import { PANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PAndamento/pAndamentoDataConfig';
import type { PAndamentoInterface } from '@/packages/administrativo/interfaces/PAndamento/PAndamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePAndamentoShowData(
  id: number,
): Promise<PAndamentoInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: PANDAMENTO_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PAndamentoInterface;
  }

  return undefined;
}

export const PAndamentoShowData = withClientErrorHandler(executePAndamentoShowData);
