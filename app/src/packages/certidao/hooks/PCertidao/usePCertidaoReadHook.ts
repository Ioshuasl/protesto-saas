import { useCallback, useState } from "react";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import { PCertidaoIndexService } from "@/packages/certidao/service/PCertidao/PCertidaoIndexService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const usePCertidaoReadHook = () => {
  const { setResponse } = useResponse();
  const [certidoes, setCertidoes] = useState<PCertidaoInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchCertidoes = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PCertidaoIndexService();

      if (Array.isArray(response)) {
        setCertidoes(response);
        setResponse({
          status: 200,
          message: "Certidões listadas com sucesso",
        });
      } else {
        setCertidoes([]);
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
  }, [setResponse]);

  return { certidoes, setCertidoes, isLoading, fetchCertidoes };
};
