'use server';

import { PTituloIntimacaoData } from '@/packages/administrativo/data/PTitulo/PTituloIntimacaoData';
import type { PTituloIntimacaoInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloIntimacaoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloIntimacaoService(id: number, payload: PTituloIntimacaoInterface) {
  const response = await PTituloIntimacaoData(id, payload);

  return response;
}

export const PTituloIntimacaoService = withClientErrorHandler(executePTituloIntimacaoService);
