'use server';

import { PPESSOA_ENDPOINTS } from '@/packages/administrativo/data/PPessoa/ppessoaDataConfig';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePPessoaDeleteData(id: number) {
  const api = new API();
  return api.send({
    method: Methods.DELETE,
    endpoint: PPESSOA_ENDPOINTS.delete(id),
  });
}

export const PPessoaDeleteData = withClientErrorHandler(executePPessoaDeleteData);
