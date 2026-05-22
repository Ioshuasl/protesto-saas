'use server';

import { PAndamentoIndexByTituloData } from '@/packages/administrativo/data/PAndamento/PAndamentoIndexByTituloData';
import type { PAndamentoIndexQuery } from '@/packages/administrativo/interfaces/PAndamento/PAndamentoIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePAndamentoIndexByTituloService(
  tituloId: number,
  query?: Omit<PAndamentoIndexQuery, 'titulo_id'>,
) {
  return await PAndamentoIndexByTituloData(tituloId, query);
}

export const PAndamentoIndexByTituloService = withClientErrorHandler(
  executePAndamentoIndexByTituloService,
);
