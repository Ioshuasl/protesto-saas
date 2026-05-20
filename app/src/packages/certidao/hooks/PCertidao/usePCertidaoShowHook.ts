import { useCallback, useState } from "react";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import { PCertidaoShowService } from "@/packages/certidao/service/PCertidao/PCertidaoShowService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const usePCertidaoShowHook = () => {
  const { setResponse } = useResponse();
  const [certidao, setCertidao] = useState<PCertidaoInterface | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchCertidao = useCallback(
    async (certidaoId: number) => {
      setIsLoading(true);
      try {
        const response = await PCertidaoShowService(certidaoId);

        if (response && typeof response === "object" && "certidao_id" in response) {
          setCertidao(response as PCertidaoInterface);
          setResponse({
            status: 200,
            message: "Certidão carregada com sucesso",
          });
        } else {
          setCertidao(null);
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
    },
    [setResponse],
  );

  return { certidao, setCertidao, isLoading, fetchCertidao };
};
