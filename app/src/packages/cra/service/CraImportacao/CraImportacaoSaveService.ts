"use server";

import { CraImportacaoSaveData } from "@/packages/cra/data/CraImportacao/CraImportacaoSaveData";
import type { CraImportacaoSavePayload } from "@/packages/cra/interface/CraImportacao/CraImportacaoSaveInterface";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executeCraImportacaoSaveService(data: CraImportacaoSavePayload) {
  const response = await CraImportacaoSaveData(data);

  return response;
}

export const CraImportacaoSaveService = withClientErrorHandler(executeCraImportacaoSaveService);
