"use server";

import { PCertidaoIndexData } from "@/packages/certidao/data/PCertidao/PCertidaoIndexData";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePCertidaoIndexService() {
  const response = await PCertidaoIndexData();

  return response;
}

export const PCertidaoIndexService = withClientErrorHandler(executePCertidaoIndexService);
