"use server";

import { PTituloIntimacaoBatchIndexData } from "@/packages/intimacao-lote/data/PTituloIntimacaoBatch/PTituloIntimacaoBatchIndexData";
import type { PTituloIndexQuery } from "@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePTituloIntimacaoBatchIndexService(query?: PTituloIndexQuery) {
  const response = await PTituloIntimacaoBatchIndexData(query);

  return response;
}

export const PTituloIntimacaoBatchIndexService = withClientErrorHandler(executePTituloIntimacaoBatchIndexService);
