"use server";

import { PRetornoCraIndexData } from "@/packages/cra/data/PRetornoCra/PRetornoCraIndexData";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePRetornoCraIndexService() {
  const response = await PRetornoCraIndexData();

  return response;
}

export const PRetornoCraIndexService = withClientErrorHandler(executePRetornoCraIndexService);
