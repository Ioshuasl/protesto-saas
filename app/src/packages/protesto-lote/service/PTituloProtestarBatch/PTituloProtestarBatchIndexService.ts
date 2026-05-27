"use server";

import { PTituloProtestarBatchIndexData } from "@/packages/protesto-lote/data/PTituloProtestarBatch/PTituloProtestarBatchIndexData";
import type { PTituloIndexQuery } from "@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePTituloProtestarBatchIndexService(query?: PTituloIndexQuery) {
  const response = await PTituloProtestarBatchIndexData(query);

  return response;
}

export const PTituloProtestarBatchIndexService = withClientErrorHandler(executePTituloProtestarBatchIndexService);
