'use server';

import { PAndamentoIndexData } from '@/packages/administrativo/data/PAndamento/PAndamentoIndexData';
import type { PAndamentoIndexQuery } from '@/packages/administrativo/interfaces/PAndamento/PAndamentoIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePAndamentoIndexService(query?: PAndamentoIndexQuery) {
  return await PAndamentoIndexData(query);
}

export const PAndamentoIndexService = withClientErrorHandler(executePAndamentoIndexService);
