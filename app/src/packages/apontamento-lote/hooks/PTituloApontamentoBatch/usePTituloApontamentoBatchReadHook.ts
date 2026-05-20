import { useCallback, useState } from "react";
import type { PTituloApontamentoBatchInterface } from "@/packages/apontamento-lote/interface/PTituloApontamentoBatch/PTituloApontamentoBatchInterface";
import { PTituloApontamentoBatchIndexService } from "@/packages/apontamento-lote/service/PTituloApontamentoBatch/PTituloApontamentoBatchIndexService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const usePTituloApontamentoBatchReadHook = () => {
  const { setResponse } = useResponse();
  const [titulosApontamentoBatch, setTitulosApontamentoBatch] = useState<PTituloApontamentoBatchInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchTitulosApontamentoBatch = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PTituloApontamentoBatchIndexService();

      if (Array.isArray(response)) {
        setTitulosApontamentoBatch(response);
        setResponse({
          status: 200,
          message: "Títulos para apontamento em lote listados com sucesso",
        });
      } else {
        setTitulosApontamentoBatch([]);
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

  return { titulosApontamentoBatch, setTitulosApontamentoBatch, isLoading, fetchTitulosApontamentoBatch };
};
