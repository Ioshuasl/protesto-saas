'use server';

import {
  PLivroNaturezaSaveUpdateData,
  type PLivroNaturezaSavePayload,
} from '@/packages/administrativo/data/PLivroNatureza/PLivroNaturezaSaveData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroNaturezaSaveUpdateService(
  id: number,
  data: Partial<PLivroNaturezaSavePayload>,
) {
  return await PLivroNaturezaSaveUpdateData(id, data);
}

export const PLivroNaturezaSaveUpdateService = withClientErrorHandler(
  executePLivroNaturezaSaveUpdateService,
);
