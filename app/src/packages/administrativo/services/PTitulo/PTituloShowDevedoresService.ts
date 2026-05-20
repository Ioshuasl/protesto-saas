'use server';

import { PTituloShowDevedoresData } from '@/packages/administrativo/data/PTitulo/PTituloShowDevedoresData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloShowDevedoresService(tituloId: number) {
  const response = await PTituloShowDevedoresData(tituloId);

  return response;
}

export const PTituloShowDevedoresService = withClientErrorHandler(executePTituloShowDevedoresService);

