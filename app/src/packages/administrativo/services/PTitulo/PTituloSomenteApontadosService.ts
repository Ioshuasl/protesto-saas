'use server';

import { PTituloSomenteApontadosData } from '@/packages/administrativo/data/PTitulo/PTituloSomenteApontadosData';
import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloSomenteApontadosService(query?: PTituloIndexQuery) {
  return await PTituloSomenteApontadosData(query);
}

export const PTituloSomenteApontadosService = withClientErrorHandler(
  executePTituloSomenteApontadosService,
);
