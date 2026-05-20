'use server';

import { PEspecieIndexData } from '@/packages/administrativo/data/PEspecie/PEspecieIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePEspecieIndexService() {
  const response = await PEspecieIndexData();

  return response;
}

export const PEspecieIndexService = withClientErrorHandler(executePEspecieIndexService);
