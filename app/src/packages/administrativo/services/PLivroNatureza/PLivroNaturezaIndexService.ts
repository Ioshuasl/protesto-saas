'use server';

import { PLivroNaturezaIndexData } from '@/packages/administrativo/data/PLivroNatureza/PLivroNaturezaIndexData';
import type { PLivroNaturezaIndexQuery } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroNaturezaIndexService(query?: PLivroNaturezaIndexQuery) {
  return await PLivroNaturezaIndexData(query);
}

export const PLivroNaturezaIndexService = withClientErrorHandler(
  executePLivroNaturezaIndexService,
);
