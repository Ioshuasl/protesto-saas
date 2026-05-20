'use server';

import { PPessoaSaveUpdateData } from '@/packages/administrativo/data/PPessoa/PPessoaSaveData';
import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePPessoaSaveUpdateService(id: number, data: Partial<PPessoaInterface>) {
  const response = await PPessoaSaveUpdateData(id, data);

  return response;
}

export const PPessoaSaveUpdateService = withClientErrorHandler(executePPessoaSaveUpdateService);
