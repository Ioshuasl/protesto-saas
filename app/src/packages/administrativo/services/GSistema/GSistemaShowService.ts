'use server';

import { GSistemaShowData } from '@/packages/administrativo/data/GSistema/GSistemaShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGSistemaShowService(id: number) {
  const response = await GSistemaShowData(id);

  return response;
}

export const GSistemaShowService = withClientErrorHandler(executeGSistemaShowService);
