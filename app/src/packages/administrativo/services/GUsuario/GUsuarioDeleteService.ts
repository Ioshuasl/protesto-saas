'use server';

import { GUsuarioDeleteData } from '@/packages/administrativo/data/GUsuario/GUsuarioDeleteData';
import type { GUsuarioInterface } from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGUsuarioDeleteService(data: GUsuarioInterface) {
  const response = await GUsuarioDeleteData(data);

  return response;
}

export const GUsuarioDeleteService = withClientErrorHandler(executeGUsuarioDeleteService);
