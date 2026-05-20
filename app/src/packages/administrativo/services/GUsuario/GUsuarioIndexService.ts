'use server';

import { GUsuarioIndexData } from '@/packages/administrativo/data/GUsuario/GUsuarioIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGUsuarioIndexService() {
  const response = await GUsuarioIndexData();

  return response;
}

export const GUsuarioIndexService = withClientErrorHandler(executeGUsuarioIndexService);
