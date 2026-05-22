'use server';

import {
  PMotivosCancelamentoSaveUpdateData,
  type PMotivosCancelamentoSavePayload,
} from '@/packages/administrativo/data/PMotivosCancelamento/PMotivosCancelamentoSaveData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosCancelamentoSaveUpdateService(
  id: number,
  data: Partial<PMotivosCancelamentoSavePayload>,
) {
  return await PMotivosCancelamentoSaveUpdateData(id, data);
}

export const PMotivosCancelamentoSaveUpdateService = withClientErrorHandler(
  executePMotivosCancelamentoSaveUpdateService,
);
