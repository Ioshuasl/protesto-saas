"use server";

import {
  PTituloArquivoShowData,
  type PArquivoTituloShowQuery,
} from "@/packages/cra/data/PTituloArquivo/PTituloArquivoShowData";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePTituloArquivoShowService(
  arquivoTituloId: number,
  query?: PArquivoTituloShowQuery,
) {
  return PTituloArquivoShowData(arquivoTituloId, query);
}

export const PTituloArquivoShowService = withClientErrorHandler(executePTituloArquivoShowService);
