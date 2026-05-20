import { useCallback, useState } from "react";
import type { PTituloInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";
import { PRetornoCraIndexService } from "@/packages/cra/service/PRetornoCra/PRetornoCraIndexService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const usePRetornoCraReadHook = () => {
  const { setResponse } = useResponse();
  const [titulosRetorno, setTitulosRetorno] = useState<PTituloInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchTitulosRetorno = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PRetornoCraIndexService();
      if (Array.isArray(response)) {
        setTitulosRetorno(response);
        setResponse({
          status: 200,
          message: "Títulos de retorno listados com sucesso",
        });
      } else {
        setTitulosRetorno([]);
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

  return { titulosRetorno, setTitulosRetorno, isLoading, fetchTitulosRetorno };
};
