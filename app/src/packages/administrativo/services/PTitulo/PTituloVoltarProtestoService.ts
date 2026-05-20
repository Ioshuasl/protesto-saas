'use server';

import { PTituloVoltarProtestoData } from '@/packages/administrativo/data/PTitulo/PTituloVoltarProtestoData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloVoltarProtestoService(id: number) {
  const response = await PTituloVoltarProtestoData(id);

  return response;
}

export const PTituloVoltarProtestoService = withClientErrorHandler(executePTituloVoltarProtestoService);
