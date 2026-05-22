'use server';

import { POcorrenciaAndamentoShowData } from '@/packages/administrativo/data/POcorrenciaAndamento/POcorrenciaAndamentoShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePOcorrenciaAndamentoShowService(id: number) {
  return await POcorrenciaAndamentoShowData(id);
}

export const POcorrenciaAndamentoShowService = withClientErrorHandler(
  executePOcorrenciaAndamentoShowService,
);
