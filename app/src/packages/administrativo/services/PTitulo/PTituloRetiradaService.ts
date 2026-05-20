'use server';

import { PTituloRetiradaData } from '@/packages/administrativo/data/PTitulo/PTituloRetiradaData';
import type { PTituloRetiradaFormInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloRetiradaFormInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloRetiradaService(id: number, payload: PTituloRetiradaFormInterface) {
  return PTituloRetiradaData(id, payload);
}

export const PTituloRetiradaService = withClientErrorHandler(executePTituloRetiradaService);
