"use server";

import { PCertidaoCancelarData } from "@/packages/certidao/data/PCertidao/PCertidaoCancelarData";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePCertidaoCancelarService(certidaoId: number) {
  return PCertidaoCancelarData(certidaoId);
}

export const PCertidaoCancelarService = withClientErrorHandler(executePCertidaoCancelarService);
