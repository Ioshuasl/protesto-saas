'use server';

import { PBancoSaveUpdateData } from '@/packages/administrativo/data/PBanco/PBancoSaveData';
import type { PBancoInterface } from '@/packages/administrativo/interfaces/PBanco/PBancoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePBancoSaveUpdateService(id: number, data: Partial<PBancoInterface>) {
  const response = await PBancoSaveUpdateData(id, data);

  return response;
}

export const PBancoSaveUpdateService = withClientErrorHandler(executePBancoSaveUpdateService);
