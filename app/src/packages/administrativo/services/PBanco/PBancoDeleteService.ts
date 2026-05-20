'use server';

import { PBancoDeleteData } from '@/packages/administrativo/data/PBanco/PBancoDeleteData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePBancoDeleteService(id: number) {
  const response = await PBancoDeleteData(id);

  return response;
}

export const PBancoDeleteService = withClientErrorHandler(executePBancoDeleteService);
