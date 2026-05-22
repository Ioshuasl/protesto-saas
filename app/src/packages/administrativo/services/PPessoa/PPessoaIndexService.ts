'use server';

import { PPessoaIndexData } from '@/packages/administrativo/data/PPessoa/PPessoaIndexData';
import type { PPessoaIndexQuery } from '@/packages/administrativo/interfaces/PPessoa/PPessoaIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePPessoaIndexService(query?: PPessoaIndexQuery) {
  return PPessoaIndexData(query);
}

export const PPessoaIndexService = withClientErrorHandler(executePPessoaIndexService);
