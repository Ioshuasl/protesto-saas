"use server";

import { PTituloArquivoShowData } from "@/packages/cra/data/PTituloArquivo/PTituloArquivoShowData";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePTituloArquivoShowService() {
  const response = await PTituloArquivoShowData();

  return response;
}

export const PTituloArquivoShowService = withClientErrorHandler(executePTituloArquivoShowService);
