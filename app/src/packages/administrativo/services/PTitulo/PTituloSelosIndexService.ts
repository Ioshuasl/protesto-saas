'use server';

import { PTituloSelosIndexData } from '@/packages/administrativo/data/PTitulo/PTituloSelosIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloSelosIndexService(id: number) {
  const response = await PTituloSelosIndexData(id);

  return response;
}

export const PTituloSelosIndexService = withClientErrorHandler(executePTituloSelosIndexService);
