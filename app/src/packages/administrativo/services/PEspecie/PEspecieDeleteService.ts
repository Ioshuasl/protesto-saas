'use server';

import { PEspecieDeleteData } from '@/packages/administrativo/data/PEspecie/PEspecieDeleteData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePEspecieDeleteService(id: number) {
  const response = await PEspecieDeleteData(id);

  return response;
}

export const PEspecieDeleteService = withClientErrorHandler(executePEspecieDeleteService);
