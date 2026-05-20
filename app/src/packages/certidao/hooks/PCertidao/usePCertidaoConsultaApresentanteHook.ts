import { useState } from "react";

import {
  isPCertidaoConsultaApresentanteResult,
  type PCertidaoConsultaApresentantePayload,
  type PCertidaoConsultaApresentanteResult,
} from "@/packages/certidao/interface/PCertidao/PCertidaoConsultaApresentanteInterface";
import { PCertidaoConsultaApresentanteService } from "@/packages/certidao/service/PCertidao/PCertidaoConsultaApresentanteService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const usePCertidaoConsultaApresentanteHook = () => {
  const { setResponse } = useResponse();
  const [analise, setAnalise] = useState<PCertidaoConsultaApresentanteResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const consultarApresentante = async (payload: PCertidaoConsultaApresentantePayload) => {
    setIsLoading(true);
    try {
      const response = await PCertidaoConsultaApresentanteService(payload);

      if (isPCertidaoConsultaApresentanteResult(response)) {
        setAnalise(response);
        setResponse({
          status: 200,
          message: "Consulta de certidão por apresentante realizada com sucesso",
        });
      } else {
        setAnalise(null);
        setResponse({
          status: (response as { status?: number }).status,
          message: (response as { message?: string }).message,
          error: (response as { message?: string }).message,
        });
      }

      return response;
    } finally {
      setIsLoading(false);
    }
  };

  const resetConsulta = () => {
    setAnalise(null);
  };

  return { analise, isLoading, consultarApresentante, resetConsulta };
};
