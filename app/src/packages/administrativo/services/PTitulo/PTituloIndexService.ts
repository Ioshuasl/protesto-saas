'use server';

import { PTituloIndexData } from '@/packages/administrativo/data/PTitulo/PTituloIndexData';
import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloIndexService(query?: PTituloIndexQuery) {
  return await PTituloIndexData(query);
}

export const PTituloIndexService = withClientErrorHandler(executePTituloIndexService);
