'use server';

import { PTituloWorkflowBatchIndexDataWithMockFallback } from '@/packages/administrativo/data/PTitulo/PTituloWorkflowBatchIndexData';
import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import { usePTituloIntimacaoBatchMockData } from '@/packages/intimacao-lote/data/PTituloIntimacaoBatch/pTituloIntimacaoBatchDataConfig';
import { pTituloIntimacaoBatchListRef } from '@/packages/intimacao-lote/data/PTituloIntimacaoBatch/pTituloIntimacaoBatchInMemory';
import type { PTituloIntimacaoBatchInterface } from '@/packages/intimacao-lote/interface/PTituloIntimacaoBatch/PTituloIntimacaoBatchInterface';

export async function PTituloIntimacaoBatchIndexData(
  query?: PTituloIndexQuery,
): Promise<PTituloIntimacaoBatchInterface[]> {
  return PTituloWorkflowBatchIndexDataWithMockFallback(
    query,
    [...pTituloIntimacaoBatchListRef.current],
    usePTituloIntimacaoBatchMockData(),
  ) as PTituloIntimacaoBatchInterface[];
}
