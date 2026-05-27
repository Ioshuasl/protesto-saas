'use server';

import { PTituloWorkflowBatchIndexDataWithMockFallback } from '@/packages/administrativo/data/PTitulo/PTituloWorkflowBatchIndexData';
import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import { usePTituloProtestarBatchMockData } from '@/packages/protesto-lote/data/PTituloProtestarBatch/pTituloProtestarBatchDataConfig';
import { pTituloProtestarBatchListRef } from '@/packages/protesto-lote/data/PTituloProtestarBatch/pTituloProtestarBatchInMemory';
import type { PTituloProtestarBatchInterface } from '@/packages/protesto-lote/interface/PTituloProtestarBatch/PTituloProtestarBatchInterface';

export async function PTituloProtestarBatchIndexData(
  query?: PTituloIndexQuery,
): Promise<PTituloProtestarBatchInterface[]> {
  return PTituloWorkflowBatchIndexDataWithMockFallback(
    query,
    [...pTituloProtestarBatchListRef.current],
    usePTituloProtestarBatchMockData(),
  ) as PTituloProtestarBatchInterface[];
}
