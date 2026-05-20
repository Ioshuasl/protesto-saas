'use server';

import { PPessoaSaveCreateData } from '@/packages/administrativo/data/PPessoa/PPessoaSaveData';
import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePPessoaSaveCreateService(data: Omit<PPessoaInterface, 'pessoa_id'>) {
  const response = await PPessoaSaveCreateData(data);

  return response;
}

export const PPessoaSaveCreateService = withClientErrorHandler(executePPessoaSaveCreateService);
