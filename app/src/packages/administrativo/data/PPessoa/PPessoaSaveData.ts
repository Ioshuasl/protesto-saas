'use server';

import { PPESSOA_ENDPOINTS } from '@/packages/administrativo/data/PPessoa/ppessoaDataConfig';
import { toPPessoaApiPayload } from '@/packages/administrativo/data/PPessoa/ppessoaApiPayload';
import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePPessoaSaveCreateData(
  data: Omit<PPessoaInterface, 'pessoa_id'>,
): Promise<PPessoaInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: PPESSOA_ENDPOINTS.create,
    body: toPPessoaApiPayload(data),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PPessoaInterface;
  }

  throw new Error(
    typeof response?.message === 'string' ? response.message : 'Erro ao cadastrar pessoa.',
  );
}

async function executePPessoaSaveUpdateData(
  id: number,
  data: Partial<PPessoaInterface>,
): Promise<PPessoaInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: PPESSOA_ENDPOINTS.update(id),
    body: toPPessoaApiPayload(data),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PPessoaInterface;
  }

  throw new Error(
    typeof response?.message === 'string' ? response.message : 'Erro ao atualizar pessoa.',
  );
}

export const PPessoaSaveCreateData = withClientErrorHandler(executePPessoaSaveCreateData);
export const PPessoaSaveUpdateData = withClientErrorHandler(executePPessoaSaveUpdateData);
