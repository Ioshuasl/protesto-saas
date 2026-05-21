'use server';

import { PLIVRO_ANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PLivroAndamento/plivroAndamentoDataConfig';
import type { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePLivroAndamentoShowData(
  id: number,
): Promise<PLivroAndamentoInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: PLIVRO_ANDAMENTO_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PLivroAndamentoInterface;
  }

  return undefined;
}

export const PLivroAndamentoShowData = withClientErrorHandler(executePLivroAndamentoShowData);
