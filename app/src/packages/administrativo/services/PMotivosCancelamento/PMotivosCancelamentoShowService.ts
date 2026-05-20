'use server';

import { PMotivosCancelamentoShowData } from '@/packages/administrativo/data/PMotivosCancelamento/PMotivosCancelamentoShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosCancelamentoShowService(id: number) {
  const response = await PMotivosCancelamentoShowData(id);

  return response;
}

export const PMotivosCancelamentoShowService = withClientErrorHandler(
  executePMotivosCancelamentoShowService,
);
