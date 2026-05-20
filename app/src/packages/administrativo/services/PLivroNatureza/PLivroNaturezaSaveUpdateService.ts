'use server';

import { PLivroNaturezaSaveUpdateData } from '@/packages/administrativo/data/PLivroNatureza/PLivroNaturezaSaveData';
import type { PLivroNaturezaInterface } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroNaturezaSaveUpdateService(
  id: number,
  data: Partial<PLivroNaturezaInterface>,
) {
  const response = await PLivroNaturezaSaveUpdateData(id, data);

  return response;
}

export const PLivroNaturezaSaveUpdateService = withClientErrorHandler(
  executePLivroNaturezaSaveUpdateService,
);
