'use server';


import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import GUsuarioIndexData from '@/packages/administrativo/data/GUsuario/GUsuarioIndexData';

async function executeGUsuarioIndexService() {
  const response = await GUsuarioIndexData();

  return response;
}

export const GUsuarioIndexService = withClientErrorHandler(executeGUsuarioIndexService);
