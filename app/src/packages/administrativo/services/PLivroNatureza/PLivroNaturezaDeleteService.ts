'use server';

import { PLivroNaturezaDeleteData } from '@/packages/administrativo/data/PLivroNatureza/PLivroNaturezaDeleteData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroNaturezaDeleteService(id: number) {
  const response = await PLivroNaturezaDeleteData(id);

  return response;
}

export const PLivroNaturezaDeleteService = withClientErrorHandler(executePLivroNaturezaDeleteService);
