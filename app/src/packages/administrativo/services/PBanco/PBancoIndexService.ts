'use server';

import { PBancoIndexData } from '@/packages/administrativo/data/PBanco/PBancoIndexData';
import type { PBancoIndexQuery } from '@/packages/administrativo/interfaces/PBanco/PBancoIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePBancoIndexService(query?: PBancoIndexQuery) {
  return await PBancoIndexData(query);
}

export const PBancoIndexService = withClientErrorHandler(executePBancoIndexService);
