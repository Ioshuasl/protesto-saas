import { useCallback, useState } from "react";
import type { PArquivoTituloShowQuery } from "@/packages/cra/data/PTituloArquivo/PTituloArquivoShowData";
import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";
import { PTituloArquivoShowService } from "@/packages/cra/service/PTituloArquivo/PTituloArquivoShowService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const usePTituloArquivoShowHook = () => {
  const { setResponse } = useResponse();
  const [arquivoTitulo, setArquivoTitulo] = useState<PArquivoTituloInterface | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchArquivoTitulo = useCallback(
    async (arquivoTituloId: number, query?: PArquivoTituloShowQuery) => {
      setIsLoading(true);
      try {
        const response = await PTituloArquivoShowService(arquivoTituloId, query);

        if (response && typeof response === "object" && "arquivo_titulo_id" in response) {
          setArquivoTitulo(response as PArquivoTituloInterface);
          setResponse({
            status: 200,
            message: "Arquivo de título carregado com sucesso",
          });
        } else {
          setArquivoTitulo(null);
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

  return { arquivoTitulo, setArquivoTitulo, isLoading, fetchArquivoTitulo };
};
