'use server';

import { PTituloSustacaoData } from '@/packages/administrativo/data/PTitulo/PTituloSustacaoData';
import type { PTituloSustacaoFormInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloSustacaoFormInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloSustacaoService(id: number, payload: PTituloSustacaoFormInterface) {
  return PTituloSustacaoData(id, payload);
}

export const PTituloSustacaoService = withClientErrorHandler(executePTituloSustacaoService);
