"use server";

import { PCertidaoConsultaApresentanteData } from "@/packages/certidao/data/PCertidao/PCertidaoConsultaApresentanteData";
import type { PCertidaoConsultaApresentantePayload } from "@/packages/certidao/interface/PCertidao/PCertidaoConsultaApresentanteInterface";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";

async function executePCertidaoConsultaApresentanteService(data: PCertidaoConsultaApresentantePayload) {
  const response = await PCertidaoConsultaApresentanteData(data);

  return response;
}

export const PCertidaoConsultaApresentanteService = withClientErrorHandler(
  executePCertidaoConsultaApresentanteService,
);
