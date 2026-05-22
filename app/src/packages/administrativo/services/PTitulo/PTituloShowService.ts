'use server';

import { PTituloShowData } from '@/packages/administrativo/data/PTitulo/PTituloShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloShowService(id: number) {
  return await PTituloShowData(id);
}

export const PTituloShowService = withClientErrorHandler(executePTituloShowService);
