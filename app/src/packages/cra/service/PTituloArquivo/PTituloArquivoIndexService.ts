"use server";

import { PTituloArquivoIndexData } from "@/packages/cra/data/PTituloArquivo/PTituloArquivoIndexData";
import type { PArquivoTituloIndexQuery } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloIndexQuery";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePTituloArquivoIndexService(query?: PArquivoTituloIndexQuery) {
  return PTituloArquivoIndexData(query);
}

export const PTituloArquivoIndexService = withClientErrorHandler(executePTituloArquivoIndexService);
