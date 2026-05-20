'use server';

import { PTituloDesistenciaData } from '@/packages/administrativo/data/PTitulo/PTituloDesistenciaData';
import type { PTituloDesistenciaFormInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloDesistenciaFormInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloDesistenciaService(id: number, payload?: PTituloDesistenciaFormInterface) {
  return PTituloDesistenciaData(id, payload);
}

export const PTituloDesistenciaService = withClientErrorHandler(
  executePTituloDesistenciaService,
);
