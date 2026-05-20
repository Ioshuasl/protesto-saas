'use server';

import { GUsuarioSaveCreateData } from '@/packages/administrativo/data/GUsuario/GUsuarioSaveData';
import type { GUsuarioInterface } from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGUsuarioSaveCreateService(data: Omit<GUsuarioInterface, 'usuario_id'>) {
  const response = await GUsuarioSaveCreateData(data);

  return response;
}

export const GUsuarioSaveCreateService = withClientErrorHandler(executeGUsuarioSaveCreateService);
