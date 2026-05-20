"use server";

import { PTituloIntimacaoBatchIndexData } from "@/packages/intimacao-lote/data/PTituloIntimacaoBatch/PTituloIntimacaoBatchIndexData";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePTituloIntimacaoBatchIndexService() {
  const response = await PTituloIntimacaoBatchIndexData();

  return response;
}

export const PTituloIntimacaoBatchIndexService = withClientErrorHandler(executePTituloIntimacaoBatchIndexService);
