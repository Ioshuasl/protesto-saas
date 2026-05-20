import { useCallback, useState } from "react";
import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";
import { PTituloArquivoShowService } from "@/packages/cra/service/PTituloArquivo/PTituloArquivoShowService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const usePTituloArquivoShowHook = () => {
  const { setResponse } = useResponse();
  const [arquivosTitulo, setArquivosTitulo] = useState<PArquivoTituloInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchArquivosTitulo = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PTituloArquivoShowService();

      if (Array.isArray(response)) {
        setArquivosTitulo(response);
        setResponse({
          status: 200,
          message: "Arquivos de título carregados com sucesso",
        });
      } else {
        setArquivosTitulo([]);
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

  return { arquivosTitulo, setArquivosTitulo, isLoading, fetchArquivosTitulo };
};
