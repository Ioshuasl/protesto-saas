'use server';

import { PTituloSomenteProtestadosData } from '@/packages/administrativo/data/PTitulo/PTituloSomenteProtestadosData';
import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloSomenteProtestadosService(query?: PTituloIndexQuery) {
  return await PTituloSomenteProtestadosData(query);
}

export const PTituloSomenteProtestadosService = withClientErrorHandler(
  executePTituloSomenteProtestadosService,
);
