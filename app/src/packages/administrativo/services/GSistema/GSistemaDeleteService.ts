'use server';

import { GSistemaDeleteData } from '@/packages/administrativo/data/GSistema/GSistemaDeleteData';
import type { GSistemaInterface } from '@/packages/administrativo/interfaces/GSistema/GSistemaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGSistemaDeleteService(data: GSistemaInterface) {
  const response = await GSistemaDeleteData(data);

  return response;
}

export const GSistemaDeleteService = withClientErrorHandler(executeGSistemaDeleteService);
