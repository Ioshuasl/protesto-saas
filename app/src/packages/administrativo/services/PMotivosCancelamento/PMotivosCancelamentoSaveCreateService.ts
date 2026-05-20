'use server';

import { PMotivosCancelamentoSaveCreateData } from '@/packages/administrativo/data/PMotivosCancelamento/PMotivosCancelamentoSaveData';
import type { PMotivosCancelamentoInterface } from '@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosCancelamentoSaveCreateService(
  data: Omit<PMotivosCancelamentoInterface, 'motivos_cancelamento_id'>,
) {
  const response = await PMotivosCancelamentoSaveCreateData(data);

  return response;
}

export const PMotivosCancelamentoSaveCreateService = withClientErrorHandler(
  executePMotivosCancelamentoSaveCreateService,
);
