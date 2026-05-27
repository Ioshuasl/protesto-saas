'use server';

import { PTituloWorkflowBatchIndexData } from '@/packages/administrativo/data/PTitulo/PTituloWorkflowBatchIndexData';
import type { PTituloBatchRowBase } from '@/packages/administrativo/data/PTitulo/ptituloIndexItemToBatchMapper';
import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloWorkflowBatchIndexService(
  query?: PTituloIndexQuery,
): Promise<PTituloBatchRowBase[]> {
  return PTituloWorkflowBatchIndexData(query);
}

export const PTituloWorkflowBatchIndexService = withClientErrorHandler(
  executePTituloWorkflowBatchIndexService,
);
