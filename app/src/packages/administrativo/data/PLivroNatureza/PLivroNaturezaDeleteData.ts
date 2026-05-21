'use server';

import { PLIVRO_NATUREZA_ENDPOINTS } from '@/packages/administrativo/data/PLivroNatureza/plivroNaturezaDataConfig';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePLivroNaturezaDeleteData(id: number) {
  const api = new API();
  return await api.send({
    method: Methods.DELETE,
    endpoint: PLIVRO_NATUREZA_ENDPOINTS.delete(id),
  });
}

export const PLivroNaturezaDeleteData = withClientErrorHandler(executePLivroNaturezaDeleteData);
