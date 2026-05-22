'use server';

import { PMotivosCancelamentoIndexData } from '@/packages/administrativo/data/PMotivosCancelamento/PMotivosCancelamentoIndexData';
import type { PMotivosCancelamentoIndexQuery } from '@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosCancelamentoIndexService(
  query?: PMotivosCancelamentoIndexQuery,
) {
  return await PMotivosCancelamentoIndexData(query);
}

export const PMotivosCancelamentoIndexService = withClientErrorHandler(
  executePMotivosCancelamentoIndexService,
);
