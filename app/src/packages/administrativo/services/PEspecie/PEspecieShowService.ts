'use server';

import { PEspecieShowData } from '@/packages/administrativo/data/PEspecie/PEspecieShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePEspecieShowService(id: number) {
  const response = await PEspecieShowData(id);

  return response;
}

export const PEspecieShowService = withClientErrorHandler(executePEspecieShowService);
