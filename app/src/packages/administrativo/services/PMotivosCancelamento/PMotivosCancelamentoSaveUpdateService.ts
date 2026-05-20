'use server';

import { PMotivosCancelamentoSaveUpdateData } from '@/packages/administrativo/data/PMotivosCancelamento/PMotivosCancelamentoSaveData';
import type { PMotivosCancelamentoInterface } from '@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosCancelamentoSaveUpdateService(
  id: number,
  data: Partial<PMotivosCancelamentoInterface>,
) {
  const response = await PMotivosCancelamentoSaveUpdateData(id, data);

  return response;
}

export const PMotivosCancelamentoSaveUpdateService = withClientErrorHandler(
  executePMotivosCancelamentoSaveUpdateService,
);
