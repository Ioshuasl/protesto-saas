'use server';

import {
  PMotivosCancelamentoSaveCreateData,
  type PMotivosCancelamentoSavePayload,
} from '@/packages/administrativo/data/PMotivosCancelamento/PMotivosCancelamentoSaveData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePMotivosCancelamentoSaveCreateService(
  data: PMotivosCancelamentoSavePayload,
) {
  return await PMotivosCancelamentoSaveCreateData(data);
}

export const PMotivosCancelamentoSaveCreateService = withClientErrorHandler(
  executePMotivosCancelamentoSaveCreateService,
);
