import { useCallback, useState } from "react";
import type { PTituloProtestarBatchInterface } from "@/packages/protesto-lote/interface/PTituloProtestarBatch/PTituloProtestarBatchInterface";
import { PTituloProtestarBatchIndexService } from "@/packages/protesto-lote/service/PTituloProtestarBatch/PTituloProtestarBatchIndexService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const usePTituloProtestarBatchReadHook = () => {
  const { setResponse } = useResponse();
  const [titulosProtestarBatch, setTitulosProtestarBatch] = useState<PTituloProtestarBatchInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchTitulosProtestarBatch = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PTituloProtestarBatchIndexService();

      if (Array.isArray(response)) {
        setTitulosProtestarBatch(response);
        setResponse({
          status: 200,
          message: "Títulos para protesto em lote listados com sucesso",
        });
      } else {
        setTitulosProtestarBatch([]);
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

  return { titulosProtestarBatch, setTitulosProtestarBatch, isLoading, fetchTitulosProtestarBatch };
};
