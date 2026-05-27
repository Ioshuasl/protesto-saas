'use server';

import { PTituloSomenteCadastradosData } from '@/packages/administrativo/data/PTitulo/PTituloSomenteCadastradosData';
import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloSomenteCadastradosService(query?: PTituloIndexQuery) {
  return await PTituloSomenteCadastradosData(query);
}

export const PTituloSomenteCadastradosService = withClientErrorHandler(
  executePTituloSomenteCadastradosService,
);
