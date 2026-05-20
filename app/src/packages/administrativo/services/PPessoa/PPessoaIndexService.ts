'use server';

import { PPessoaIndexData } from '@/packages/administrativo/data/PPessoa/PPessoaIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePPessoaIndexService() {
  const response = await PPessoaIndexData();

  return response;
}

export const PPessoaIndexService = withClientErrorHandler(executePPessoaIndexService);
