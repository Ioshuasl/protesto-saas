"use server";

import { PCertidaoShowData } from "@/packages/certidao/data/PCertidao/PCertidaoShowData";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePCertidaoShowService(certidaoId: number) {
  const response = await PCertidaoShowData(certidaoId);

  return response;
}

export const PCertidaoShowService = withClientErrorHandler(executePCertidaoShowService);
