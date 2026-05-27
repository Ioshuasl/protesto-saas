'use server';

import { PTituloSomenteIntimadosData } from '@/packages/administrativo/data/PTitulo/PTituloSomenteIntimadosData';
import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloSomenteIntimadosService(query?: PTituloIndexQuery) {
  return await PTituloSomenteIntimadosData(query);
}

export const PTituloSomenteIntimadosService = withClientErrorHandler(
  executePTituloSomenteIntimadosService,
);
