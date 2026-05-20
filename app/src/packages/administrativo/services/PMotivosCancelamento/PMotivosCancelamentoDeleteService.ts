'use server';

import { PMotivosCancelamentoDeleteData } from '@/packages/administrativo/data/PMotivosCancelamento/PMotivosCancelamentoDeleteData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosCancelamentoDeleteService(id: number) {
  const response = await PMotivosCancelamentoDeleteData(id);

  return response;
}

export const PMotivosCancelamentoDeleteService = withClientErrorHandler(
  executePMotivosCancelamentoDeleteService,
);
