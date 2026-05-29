"use server";

import { PTituloArquivoDownloadData } from "@/packages/cra/data/PTituloArquivo/PTituloArquivoDownloadData";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePTituloArquivoDownloadService(
  arquivoTituloId: number,
  fallbackFilename?: string,
) {
  return PTituloArquivoDownloadData(arquivoTituloId, fallbackFilename);
}

export const PTituloArquivoDownloadService = withClientErrorHandler(
  executePTituloArquivoDownloadService,
);
