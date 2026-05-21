'use server';

import { PLIVRO_ANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PLivroAndamento/plivroAndamentoDataConfig';
import type { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export type PLivroAndamentoSavePayload = {
  livro_natureza_id: number;
  folha_atual: number;
  numero_livro: number;
  numero_folhas: number;
  data_abertura: string;
  data_fechamento?: string | null;
  sigla?: string;
  usuario_id?: number | null;
};

async function executePLivroAndamentoSaveCreateData(
  data: PLivroAndamentoSavePayload,
): Promise<PLivroAndamentoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: PLIVRO_ANDAMENTO_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PLivroAndamentoInterface;
  }

  throw new Error(response?.message ?? 'Erro ao cadastrar livro de andamento');
}

async function executePLivroAndamentoSaveUpdateData(
  id: number,
  data: Partial<PLivroAndamentoSavePayload>,
): Promise<PLivroAndamentoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: PLIVRO_ANDAMENTO_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PLivroAndamentoInterface;
  }

  throw new Error(response?.message ?? 'Erro ao atualizar livro de andamento');
}

export const PLivroAndamentoSaveCreateData = withClientErrorHandler(
  executePLivroAndamentoSaveCreateData,
);
export const PLivroAndamentoSaveUpdateData = withClientErrorHandler(
  executePLivroAndamentoSaveUpdateData,
);
