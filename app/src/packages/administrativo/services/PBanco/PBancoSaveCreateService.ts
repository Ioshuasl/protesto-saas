'use server';

import { PBancoSaveCreateData } from '@/packages/administrativo/data/PBanco/PBancoSaveData';
import type { PBancoInterface } from '@/packages/administrativo/interfaces/PBanco/PBancoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePBancoSaveCreateService(data: Omit<PBancoInterface, 'banco_id'>) {
  const response = await PBancoSaveCreateData(data);

  return response;
}

export const PBancoSaveCreateService = withClientErrorHandler(executePBancoSaveCreateService);
