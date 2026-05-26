import { useState } from "react";

import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import { isPCertidaoSaveResult } from "@/packages/certidao/interface/PCertidao/PCertidaoSaveInterface";
import { PCertidaoCancelarService } from "@/packages/certidao/service/PCertidao/PCertidaoCancelarService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const usePCertidaoCancelarHook = () => {
  const { setResponse } = useResponse();
  const [pCertidao, setPCertidao] = useState<PCertidaoInterface | null>(null);
  const [isCanceling, setIsCanceling] = useState(false);

  const cancelarCertidao = async (certidaoId: number) => {
    setIsCanceling(true);
    try {
      const response = await PCertidaoCancelarService(certidaoId);

      if (isPCertidaoSaveResult(response)) {
        setPCertidao(response);
      }

      setResponse(
        isPCertidaoSaveResult(response)
          ? {
              status: 200,
              message: "Certidão cancelada com sucesso",
            }
          : {
              status: (response as { status?: number }).status,
              message: (response as { message?: string }).message,
              error: (response as { message?: string }).message,
            },
      );

      return response;
    } finally {
      setIsCanceling(false);
    }
  };

  return { pCertidao, isCanceling, cancelarCertidao };
};
