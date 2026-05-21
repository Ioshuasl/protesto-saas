'use server';

import { PLivroAndamentoIndexData } from '@/packages/administrativo/data/PLivroAndamento/PLivroAndamentoIndexData';
import type { PLivroAndamentoIndexQuery } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroAndamentoIndexService(query?: PLivroAndamentoIndexQuery) {
  return await PLivroAndamentoIndexData(query);
}

export const PLivroAndamentoIndexService = withClientErrorHandler(
  executePLivroAndamentoIndexService,
);
