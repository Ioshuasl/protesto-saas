'use server';

import { PLivroNaturezaIndexData } from '@/packages/administrativo/data/PLivroNatureza/PLivroNaturezaIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroNaturezaIndexService() {
  const response = await PLivroNaturezaIndexData();

  return response;
}

export const PLivroNaturezaIndexService = withClientErrorHandler(executePLivroNaturezaIndexService);
