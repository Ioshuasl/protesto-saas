'use server';

import { PTituloProximoNumeroApontamentoData } from '@/packages/administrativo/data/PTitulo/PTituloProximoNumeroApontamentoData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloProximoNumeroApontamentoService() {
  const response = await PTituloProximoNumeroApontamentoData();

  return response;
}

export const PTituloProximoNumeroApontamentoService = withClientErrorHandler(
  executePTituloProximoNumeroApontamentoService,
);
