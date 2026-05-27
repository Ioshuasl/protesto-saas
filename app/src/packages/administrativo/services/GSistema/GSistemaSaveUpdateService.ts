'use server';

import { GSistemaSaveUpdateData } from '@/packages/administrativo/data/GSistema/GSistemaSaveData';
import type { GSistemaInterface } from '@/packages/administrativo/interfaces/GSistema/GSistemaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGSistemaSaveUpdateService(
  id: number,
  data: Partial<Omit<GSistemaInterface, 'sistema_id'>>,
) {
  const response = await GSistemaSaveUpdateData(id, data);

  return response;
}

export const GSistemaSaveUpdateService = withClientErrorHandler(executeGSistemaSaveUpdateService);
