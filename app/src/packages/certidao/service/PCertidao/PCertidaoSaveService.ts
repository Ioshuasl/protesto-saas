"use server";

import { PCertidaoSaveData } from "@/packages/certidao/data/PCertidao/PCertidaoSaveData";
import type { PCertidaoSavePayload } from "@/packages/certidao/interface/PCertidao/PCertidaoSaveInterface";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePCertidaoSaveService(data: PCertidaoSavePayload) {
  const response = await PCertidaoSaveData(data);

  return response;
}

export const PCertidaoSaveService = withClientErrorHandler(executePCertidaoSaveService);
