'use server';

import { PLIVRO_ANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PLivroAndamento/plivroAndamentoDataConfig';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePLivroAndamentoDeleteData(id: number) {
  const api = new API();
  return await api.send({
    method: Methods.DELETE,
    endpoint: PLIVRO_ANDAMENTO_ENDPOINTS.delete(id),
  });
}

export const PLivroAndamentoDeleteData = withClientErrorHandler(executePLivroAndamentoDeleteData);
