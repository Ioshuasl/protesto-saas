"use server";

import { PCertidaoIndexData } from "@/packages/certidao/data/PCertidao/PCertidaoIndexData";
import type { PCertidaoIndexQuery } from "@/packages/certidao/interface/PCertidao/PCertidaoIndexQuery";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePCertidaoIndexService(query?: PCertidaoIndexQuery) {
  const response = await PCertidaoIndexData(query);

  return response;
}

export const PCertidaoIndexService = withClientErrorHandler(executePCertidaoIndexService);
