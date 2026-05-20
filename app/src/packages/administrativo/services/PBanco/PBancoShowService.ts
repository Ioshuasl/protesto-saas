'use server';

import { PBancoShowData } from '@/packages/administrativo/data/PBanco/PBancoShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePBancoShowService(id: number) {
  const response = await PBancoShowData(id);

  return response;
}

export const PBancoShowService = withClientErrorHandler(executePBancoShowService);
