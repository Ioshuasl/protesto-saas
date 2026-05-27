'use server';

import { PTituloWorkflowBatchIndexDataWithMockFallback } from '@/packages/administrativo/data/PTitulo/PTituloWorkflowBatchIndexData';
import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import { usePTituloApontamentoBatchMockData } from '@/packages/apontamento-lote/data/PTituloApontamentoBatch/pTituloApontamentoBatchDataConfig';
import { pTituloApontamentoBatchListRef } from '@/packages/apontamento-lote/data/PTituloApontamentoBatch/pTituloApontamentoBatchInMemory';
import type { PTituloApontamentoBatchInterface } from '@/packages/apontamento-lote/interface/PTituloApontamentoBatch/PTituloApontamentoBatchInterface';

export async function PTituloApontamentoBatchIndexData(
  query?: PTituloIndexQuery,
): Promise<PTituloApontamentoBatchInterface[]> {
  return PTituloWorkflowBatchIndexDataWithMockFallback(
    query,
    [...pTituloApontamentoBatchListRef.current],
    usePTituloApontamentoBatchMockData(),
  ) as PTituloApontamentoBatchInterface[];
}
