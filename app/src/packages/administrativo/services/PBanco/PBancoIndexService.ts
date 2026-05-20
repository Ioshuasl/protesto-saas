'use server';

import { PBancoIndexData } from '@/packages/administrativo/data/PBanco/PBancoIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePBancoIndexService() {
  const response = await PBancoIndexData();

  return response;
}

export const PBancoIndexService = withClientErrorHandler(executePBancoIndexService);
