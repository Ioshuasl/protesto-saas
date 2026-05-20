'use server';

import { PEspecieSaveUpdateData } from '@/packages/administrativo/data/PEspecie/PEspecieSaveData';
import type { PEspecieInterface } from '@/packages/administrativo/interfaces/PEspecie/PEspecieInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePEspecieSaveUpdateService(id: number, data: Partial<PEspecieInterface>) {
  const response = await PEspecieSaveUpdateData(id, data);

  return response;
}

export const PEspecieSaveUpdateService = withClientErrorHandler(executePEspecieSaveUpdateService);
