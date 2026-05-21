'use server';

import { PEspecieIndexData } from '@/packages/administrativo/data/PEspecie/PEspecieIndexData';
import type { PEspecieIndexQuery } from '@/packages/administrativo/interfaces/PEspecie/PEspecieIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePEspecieIndexService(query?: PEspecieIndexQuery) {
  return await PEspecieIndexData(query);
}

export const PEspecieIndexService = withClientErrorHandler(executePEspecieIndexService);
