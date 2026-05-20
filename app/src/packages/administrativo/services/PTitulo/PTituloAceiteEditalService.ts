'use server';

import { PTituloAceiteEditalData } from '@/packages/administrativo/data/PTitulo/PTituloAceiteEditalData';
import type { PTituloAceiteEditalInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloAceiteEditalInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloAceiteEditalService(id: number, payload: PTituloAceiteEditalInterface) {
  const response = await PTituloAceiteEditalData(id, payload);

  return response;
}

export const PTituloAceiteEditalService = withClientErrorHandler(
  executePTituloAceiteEditalService,
);
