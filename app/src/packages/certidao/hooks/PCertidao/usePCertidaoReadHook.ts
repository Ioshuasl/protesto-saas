import { useCallback, useState } from "react";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import type { PCertidaoIndexQuery } from "@/packages/certidao/interface/PCertidao/PCertidaoIndexQuery";
import type { PCertidaoIndexResult } from "@/packages/certidao/interface/PCertidao/PCertidaoIndexResult";
import { PCertidaoIndexService } from "@/packages/certidao/service/PCertidao/PCertidaoIndexService";
import { DEFAULT_PAGINATION_META, type PaginationMeta } from "@/shared/components/pagination";
import { useResponse } from "@/shared/components/response/ResponseContext";

function isPCertidaoIndexResult(value: unknown): value is PCertidaoIndexResult {
  return (
    typeof value === "object" &&
    value !== null &&
    Array.isArray((value as PCertidaoIndexResult).rows) &&
    typeof (value as PCertidaoIndexResult).pagination === "object"
  );
}

export const usePCertidaoReadHook = () => {
  const { setResponse } = useResponse();
  const [certidoes, setCertidoes] = useState<PCertidaoInterface[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta>(DEFAULT_PAGINATION_META);
  const [isLoading, setIsLoading] = useState(false);

  const fetchCertidoes = useCallback(async (query?: PCertidaoIndexQuery) => {
    setIsLoading(true);
    try {
      const response = await PCertidaoIndexService(query);

      if (isPCertidaoIndexResult(response)) {
        setCertidoes(response.rows);
        setPagination(response.pagination);
        setResponse({
          status: 200,
          message: "Certidões listadas com sucesso",
        });
      } else {
        setCertidoes([]);
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

  return { certidoes, pagination, setCertidoes, isLoading, fetchCertidoes };
};
