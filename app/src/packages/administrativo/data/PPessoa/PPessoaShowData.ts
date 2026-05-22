'use server';

import { PPESSOA_ENDPOINTS } from '@/packages/administrativo/data/PPessoa/ppessoaDataConfig';
import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePPessoaShowData(id: number): Promise<PPessoaInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: PPESSOA_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PPessoaInterface;
  }

  return undefined;
}

export const PPessoaShowData = withClientErrorHandler(executePPessoaShowData);
