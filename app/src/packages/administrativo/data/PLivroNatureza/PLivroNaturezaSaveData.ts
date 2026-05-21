'use server';

import { PLIVRO_NATUREZA_ENDPOINTS } from '@/packages/administrativo/data/PLivroNatureza/plivroNaturezaDataConfig';
import type { PLivroNaturezaInterface } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export type PLivroNaturezaSavePayload = Pick<
  PLivroNaturezaInterface,
  'sigla' | 'descricao' | 'situacao'
>;

async function executePLivroNaturezaSaveCreateData(
  data: PLivroNaturezaSavePayload,
): Promise<PLivroNaturezaInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: PLIVRO_NATUREZA_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PLivroNaturezaInterface;
  }

  throw new Error(response?.message ?? 'Erro ao cadastrar natureza de livro');
}

async function executePLivroNaturezaSaveUpdateData(
  id: number,
  data: Partial<PLivroNaturezaSavePayload>,
): Promise<PLivroNaturezaInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: PLIVRO_NATUREZA_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PLivroNaturezaInterface;
  }

  throw new Error(response?.message ?? 'Erro ao atualizar natureza de livro');
}

export const PLivroNaturezaSaveCreateData = withClientErrorHandler(
  executePLivroNaturezaSaveCreateData,
);
export const PLivroNaturezaSaveUpdateData = withClientErrorHandler(
  executePLivroNaturezaSaveUpdateData,
);
