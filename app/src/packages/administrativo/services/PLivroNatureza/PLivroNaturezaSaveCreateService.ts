'use server';

import { PLivroNaturezaSaveCreateData } from '@/packages/administrativo/data/PLivroNatureza/PLivroNaturezaSaveData';
import type { PLivroNaturezaInterface } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroNaturezaSaveCreateService(
  data: Omit<PLivroNaturezaInterface, 'livro_natureza_id'>,
) {
  const response = await PLivroNaturezaSaveCreateData(data);

  return response;
}

export const PLivroNaturezaSaveCreateService = withClientErrorHandler(
  executePLivroNaturezaSaveCreateService,
);
