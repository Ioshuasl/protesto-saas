"use server";

import { PTituloArquivoIndexData } from "@/packages/cra/data/PTituloArquivo/PTituloArquivoIndexData";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePTituloArquivoIndexService() {
  const response = await PTituloArquivoIndexData();

  return response;
}

export const PTituloArquivoIndexService = withClientErrorHandler(executePTituloArquivoIndexService);
