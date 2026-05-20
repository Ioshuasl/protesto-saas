'use server';

import { PTituloShowData } from '@/packages/administrativo/data/PTitulo/PTituloShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloShowService(id: number) {
  const response = await PTituloShowData(id);

  return response;
}

export const PTituloShowService = withClientErrorHandler(executePTituloShowService);
