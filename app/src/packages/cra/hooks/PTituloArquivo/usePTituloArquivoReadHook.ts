import { useCallback, useState } from "react";
import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";
import type { PArquivoTituloIndexQuery } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloIndexQuery";
import type { PArquivoTituloIndexResult } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloIndexQuery";
import { PTituloArquivoIndexService } from "@/packages/cra/service/PTituloArquivo/PTituloArquivoIndexService";
import { DEFAULT_PAGINATION_META, type PaginationMeta } from "@/shared/components/pagination";
import { useResponse } from "@/shared/components/response/ResponseContext";

function isPArquivoTituloIndexResult(value: unknown): value is PArquivoTituloIndexResult {
  return (
    typeof value === "object" &&
    value !== null &&
    Array.isArray((value as PArquivoTituloIndexResult).rows) &&
    typeof (value as PArquivoTituloIndexResult).pagination === "object"
  );
}

export const usePTituloArquivoReadHook = () => {
  const { setResponse } = useResponse();
  const [arquivosTitulo, setArquivosTitulo] = useState<PArquivoTituloInterface[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta>(DEFAULT_PAGINATION_META);
  const [isLoading, setIsLoading] = useState(false);

  const fetchArquivosTitulo = useCallback(async (query?: PArquivoTituloIndexQuery) => {
    setIsLoading(true);
    try {
      const response = await PTituloArquivoIndexService(query);

      if (isPArquivoTituloIndexResult(response)) {
        setArquivosTitulo(response.rows);
        setPagination(response.pagination);
        setResponse({
          status: 200,
          message: "Arquivos de título listados com sucesso",
        });
      } else {
        setArquivosTitulo([]);
        setPagination(DEFAULT_PAGINATION_META);
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

  return { arquivosTitulo, pagination, setArquivosTitulo, isLoading, fetchArquivosTitulo };
};
