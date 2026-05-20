"use server";

import { PTituloApontamentoBatchIndexData } from "@/packages/apontamento-lote/data/PTituloApontamentoBatch/PTituloApontamentoBatchIndexData";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePTituloApontamentoBatchIndexService() {
  const response = await PTituloApontamentoBatchIndexData();

  return response;
}

export const PTituloApontamentoBatchIndexService = withClientErrorHandler(
  executePTituloApontamentoBatchIndexService,
);
