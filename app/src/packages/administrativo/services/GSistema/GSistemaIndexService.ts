'use server';

import { GSistemaIndexData } from '@/packages/administrativo/data/GSistema/GSistemaIndexData';
import type { GSistemaIndexQuery } from '@/packages/administrativo/interfaces/GSistema/GSistemaIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGSistemaIndexService(query?: GSistemaIndexQuery) {
  const response = await GSistemaIndexData(query);

  return response;
}

export const GSistemaIndexService = withClientErrorHandler(executeGSistemaIndexService);
