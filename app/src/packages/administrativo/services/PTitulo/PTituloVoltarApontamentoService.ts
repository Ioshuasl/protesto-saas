'use server';

import { PTituloVoltarApontamentoData } from '@/packages/administrativo/data/PTitulo/PTituloVoltarApontamentoData';
import type { PTituloVoltarApontamentoInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloVoltarApontamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloVoltarApontamentoService(
  id: number,
  payload: PTituloVoltarApontamentoInterface,
) {
  const response = await PTituloVoltarApontamentoData(id, payload);

  return response;
}

export const PTituloVoltarApontamentoService = withClientErrorHandler(
  executePTituloVoltarApontamentoService,
);
