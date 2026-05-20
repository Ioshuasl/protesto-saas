'use server';

import { PTituloIndexData } from '@/packages/administrativo/data/PTitulo/PTituloIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloIndexService() {
  const response = await PTituloIndexData();

  return response;
}

export const PTituloIndexService = withClientErrorHandler(executePTituloIndexService);
