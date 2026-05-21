'use server';

import { PLIVRO_ANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PLivroAndamento/plivroAndamentoDataConfig';
import type { PLivroAndamentoProximoNumero } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoProximoNumero';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePLivroAndamentoProximoNumeroData(
  livroNaturezaId: number,
): Promise<PLivroAndamentoProximoNumero | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: PLIVRO_ANDAMENTO_ENDPOINTS.proximoNumeroLivro(livroNaturezaId),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PLivroAndamentoProximoNumero;
  }

  return undefined;
}

export const PLivroAndamentoProximoNumeroData = withClientErrorHandler(
  executePLivroAndamentoProximoNumeroData,
);
