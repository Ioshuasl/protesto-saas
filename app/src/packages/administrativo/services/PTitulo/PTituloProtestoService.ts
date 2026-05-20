'use server';

import { PTituloProtestoData } from '@/packages/administrativo/data/PTitulo/PTituloProtestoData';
import type { PTituloProtestoInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloProtestoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloProtestoService(id: number, payload: PTituloProtestoInterface) {
  const response = await PTituloProtestoData(id, payload);

  return response;
}

export const PTituloProtestoService = withClientErrorHandler(executePTituloProtestoService);
