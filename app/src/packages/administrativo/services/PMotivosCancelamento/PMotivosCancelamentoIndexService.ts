'use server';

import { PMotivosCancelamentoIndexData } from '@/packages/administrativo/data/PMotivosCancelamento/PMotivosCancelamentoIndexData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosCancelamentoIndexService() {
  const response = await PMotivosCancelamentoIndexData();

  return response;
}

export const PMotivosCancelamentoIndexService = withClientErrorHandler(
  executePMotivosCancelamentoIndexService,
);
