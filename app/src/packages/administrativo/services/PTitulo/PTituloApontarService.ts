'use server';

import { PTituloApontarData } from '@/packages/administrativo/data/PTitulo/PTituloApontarData';
import type { PTituloApontarInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloApontarInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloApontarService(id: number, payload: PTituloApontarInterface) {
  const response = await PTituloApontarData(id, payload);

  return response;
}

export const PTituloApontarService = withClientErrorHandler(executePTituloApontarService);
