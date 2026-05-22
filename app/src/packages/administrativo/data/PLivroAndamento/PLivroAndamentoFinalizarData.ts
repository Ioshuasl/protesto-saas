'use server';

import { PLIVRO_ANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PLivroAndamento/plivroAndamentoDataConfig';
import type { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export type PLivroAndamentoFinalizarPayload = {
  data_fechamento: string;
  folha_atual?: number;
  usuario_id?: number | null;
};

async function executePLivroAndamentoFinalizarData(
  id: number,
  data: PLivroAndamentoFinalizarPayload,
): Promise<PLivroAndamentoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: PLIVRO_ANDAMENTO_ENDPOINTS.finalizar(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PLivroAndamentoInterface;
  }

  throw new Error(response?.message ?? 'Erro ao finalizar livro de andamento');
}

export const PLivroAndamentoFinalizarData = withClientErrorHandler(
  executePLivroAndamentoFinalizarData,
);
