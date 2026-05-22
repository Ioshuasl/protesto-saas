'use server';

import { POcorrenciaAndamentoIndexData } from '@/packages/administrativo/data/POcorrenciaAndamento/POcorrenciaAndamentoIndexData';
import type { POcorrenciaAndamentoIndexQuery } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePOcorrenciaAndamentoIndexService(
  query?: POcorrenciaAndamentoIndexQuery,
) {
  return await POcorrenciaAndamentoIndexData(query);
}

export const POcorrenciaAndamentoIndexService = withClientErrorHandler(
  executePOcorrenciaAndamentoIndexService,
);
