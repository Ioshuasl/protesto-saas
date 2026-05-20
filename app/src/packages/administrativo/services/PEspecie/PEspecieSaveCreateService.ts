'use server';

import { PEspecieSaveCreateData } from '@/packages/administrativo/data/PEspecie/PEspecieSaveData';
import type { PEspecieInterface } from '@/packages/administrativo/interfaces/PEspecie/PEspecieInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePEspecieSaveCreateService(data: Omit<PEspecieInterface, 'especie_id'>) {
  const response = await PEspecieSaveCreateData(data);

  return response;
}

export const PEspecieSaveCreateService = withClientErrorHandler(executePEspecieSaveCreateService);
