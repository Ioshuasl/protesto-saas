'use server';

import { PBancoShowByCodigoData } from '@/packages/administrativo/data/PBanco/PBancoShowByCodigoData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePBancoShowByCodigoService(codigoBanco: string) {
  return await PBancoShowByCodigoData(codigoBanco);
}

export const PBancoShowByCodigoService = withClientErrorHandler(executePBancoShowByCodigoService);
