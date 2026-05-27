"use server";

import { PTituloApontamentoBatchIndexData } from "@/packages/apontamento-lote/data/PTituloApontamentoBatch/PTituloApontamentoBatchIndexData";
import type { PTituloIndexQuery } from "@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePTituloApontamentoBatchIndexService(query?: PTituloIndexQuery) {
  const response = await PTituloApontamentoBatchIndexData(query);

  return response;
}

export const PTituloApontamentoBatchIndexService = withClientErrorHandler(
  executePTituloApontamentoBatchIndexService,
);
