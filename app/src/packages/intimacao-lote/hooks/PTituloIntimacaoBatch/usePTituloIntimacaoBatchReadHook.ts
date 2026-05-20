import { useCallback, useState } from "react";
import type { PTituloIntimacaoBatchInterface } from "@/packages/intimacao-lote/interface/PTituloIntimacaoBatch/PTituloIntimacaoBatchInterface";
import { PTituloIntimacaoBatchIndexService } from "@/packages/intimacao-lote/service/PTituloIntimacaoBatch/PTituloIntimacaoBatchIndexService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const usePTituloIntimacaoBatchReadHook = () => {
  const { setResponse } = useResponse();
  const [titulosIntimacaoBatch, setTitulosIntimacaoBatch] = useState<PTituloIntimacaoBatchInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchTitulosIntimacaoBatch = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PTituloIntimacaoBatchIndexService();

      if (Array.isArray(response)) {
        setTitulosIntimacaoBatch(response);
        setResponse({
          status: 200,
          message: "Títulos para intimação em lote listados com sucesso",
        });
      } else {
        setTitulosIntimacaoBatch([]);
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

  return { titulosIntimacaoBatch, setTitulosIntimacaoBatch, isLoading, fetchTitulosIntimacaoBatch };
};
