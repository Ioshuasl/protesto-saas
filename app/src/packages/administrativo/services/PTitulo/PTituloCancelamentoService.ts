'use server';

import { PTituloCancelamentoData } from '@/packages/administrativo/data/PTitulo/PTituloCancelamentoData';
import type { PTituloCancelamentoFormInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloCancelamentoFormInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloCancelamentoService(id: number, payload?: PTituloCancelamentoFormInterface) {
  return PTituloCancelamentoData(id, payload);
}

export const PTituloCancelamentoService = withClientErrorHandler(
  executePTituloCancelamentoService,
);
