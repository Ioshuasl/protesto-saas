import { useCallback, useState } from "react";

import { isTituloListItem, type TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import { PTituloShowService } from "@/packages/administrativo/services/PTitulo/PTituloShowService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const usePTituloShowHook = () => {
  const { setResponse } = useResponse();
  const [titulo, setTitulo] = useState<TituloListItem | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchTituloById = useCallback(
    async (tituloId: number) => {
      setIsLoading(true);
      try {
        const response = await PTituloShowService(tituloId);

        if (isTituloListItem(response)) {
          setTitulo(response);
          setResponse({
            status: 200,
            message: "Título carregado com sucesso",
          });
        } else {
          setTitulo(null);
          setResponse({
            status: response.status,
            message: response.message,
            error: response.message,
          });
        }

        return response;
      } finally {
        setIsLoading(false);
      }
    },
    [setResponse],
  );

  return { titulo, setTitulo, isLoading, fetchTituloById };
};
