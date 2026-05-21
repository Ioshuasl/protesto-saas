'use server';

import {
  PLivroNaturezaSaveCreateData,
  type PLivroNaturezaSavePayload,
} from '@/packages/administrativo/data/PLivroNatureza/PLivroNaturezaSaveData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroNaturezaSaveCreateService(data: PLivroNaturezaSavePayload) {
  return await PLivroNaturezaSaveCreateData(data);
}

export const PLivroNaturezaSaveCreateService = withClientErrorHandler(
  executePLivroNaturezaSaveCreateService,
);
