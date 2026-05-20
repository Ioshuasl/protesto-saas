'use server';

import { PLivroNaturezaShowData } from '@/packages/administrativo/data/PLivroNatureza/PLivroNaturezaShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroNaturezaShowService(id: number) {
  const response = await PLivroNaturezaShowData(id);

  return response;
}

export const PLivroNaturezaShowService = withClientErrorHandler(executePLivroNaturezaShowService);
