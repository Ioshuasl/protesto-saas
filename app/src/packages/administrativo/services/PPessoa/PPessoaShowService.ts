'use server';

import { PPessoaShowData } from '@/packages/administrativo/data/PPessoa/PPessoaShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePPessoaShowService(id: number) {
  const response = await PPessoaShowData(id);

  return response;
}

export const PPessoaShowService = withClientErrorHandler(executePPessoaShowService);
