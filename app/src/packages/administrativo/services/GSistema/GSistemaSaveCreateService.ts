'use server';

import { GSistemaSaveCreateData } from '@/packages/administrativo/data/GSistema/GSistemaSaveData';
import type { GSistemaInterface } from '@/packages/administrativo/interfaces/GSistema/GSistemaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGSistemaSaveCreateService(data: GSistemaInterface) {
  const response = await GSistemaSaveCreateData(data);

  return response;
}

export const GSistemaSaveCreateService = withClientErrorHandler(executeGSistemaSaveCreateService);
