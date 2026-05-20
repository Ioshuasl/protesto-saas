'use server';

import { GUsuarioShowData } from '@/packages/administrativo/data/GUsuario/GUsuarioShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGUsuarioShowService(id: number) {
  const response = await GUsuarioShowData(id);

  return response;
}

export const GUsuarioShowService = withClientErrorHandler(executeGUsuarioShowService);
