'use server';

import { GUsuarioSaveUpdateData } from '@/packages/administrativo/data/GUsuario/GUsuarioSaveData';
import type { GUsuarioInterface } from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGUsuarioSaveUpdateService(id: number, data: Partial<GUsuarioInterface>) {
  const response = await GUsuarioSaveUpdateData(id, data);

  return response;
}

export const GUsuarioSaveUpdateService = withClientErrorHandler(executeGUsuarioSaveUpdateService);
