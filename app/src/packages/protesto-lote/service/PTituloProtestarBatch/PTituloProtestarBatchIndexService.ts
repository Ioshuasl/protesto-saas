"use server";

import { PTituloProtestarBatchIndexData } from "@/packages/protesto-lote/data/PTituloProtestarBatch/PTituloProtestarBatchIndexData";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePTituloProtestarBatchIndexService() {
  const response = await PTituloProtestarBatchIndexData();

  return response;
}

export const PTituloProtestarBatchIndexService = withClientErrorHandler(executePTituloProtestarBatchIndexService);
