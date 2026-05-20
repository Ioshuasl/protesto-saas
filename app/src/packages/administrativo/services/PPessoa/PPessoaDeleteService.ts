'use server';

import { PPessoaDeleteData } from '@/packages/administrativo/data/PPessoa/PPessoaDeleteData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePPessoaDeleteService(id: number) {
  const response = await PPessoaDeleteData(id);

  return response;
}

export const PPessoaDeleteService = withClientErrorHandler(executePPessoaDeleteService);
