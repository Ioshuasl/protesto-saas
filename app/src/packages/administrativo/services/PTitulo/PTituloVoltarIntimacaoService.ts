'use server';

import { PTituloVoltarIntimacaoData } from '@/packages/administrativo/data/PTitulo/PTituloVoltarIntimacaoData';
import type { PTituloVoltarIntimacaoInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloVoltarIntimacaoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloVoltarIntimacaoService(
  id: number,
  payload: PTituloVoltarIntimacaoInterface,
) {
  const response = await PTituloVoltarIntimacaoData(id, payload);

  return response;
}

export const PTituloVoltarIntimacaoService = withClientErrorHandler(
  executePTituloVoltarIntimacaoService,
);
