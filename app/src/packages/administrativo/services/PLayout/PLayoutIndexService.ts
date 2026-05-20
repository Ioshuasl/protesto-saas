'use server';

import { PLayoutIndexData } from "@/packages/administrativo/data/PLayout/PLayoutIndexData";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePLayoutIndexService() {
  const response = await PLayoutIndexData();

  return response;
}

export const PLayoutIndexService = withClientErrorHandler(executePLayoutIndexService);
