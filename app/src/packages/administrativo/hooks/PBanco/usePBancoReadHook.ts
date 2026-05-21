import { useCallback, useState } from 'react';

import type { PBancoInterface } from '@/packages/administrativo/interfaces/PBanco/PBancoInterface';
import type { PBancoIndexQuery } from '@/packages/administrativo/interfaces/PBanco/PBancoIndexQuery';
import type { PBancoIndexResult } from '@/packages/administrativo/interfaces/PBanco/PBancoIndexResult';
import { PBancoIndexService } from '@/packages/administrativo/services/PBanco/PBancoIndexService';
import { DEFAULT_PAGINATION_META, type PaginationMeta } from '@/shared/components/pagination';
import { useResponse } from '@/shared/components/response/ResponseContext';

function isPBancoIndexResult(value: unknown): value is PBancoIndexResult {
  return (
    typeof value === 'object' &&
    value !== null &&
    Array.isArray((value as PBancoIndexResult).rows) &&
    typeof (value as PBancoIndexResult).pagination === 'object'
  );
}

export const usePBancoReadHook = () => {
  const { setResponse } = useResponse();
  const [bancos, setBancos] = useState<PBancoInterface[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta>(DEFAULT_PAGINATION_META);
  const [isLoading, setIsLoading] = useState(false);

  const fetchBancos = useCallback(async (query?: PBancoIndexQuery) => {
    setIsLoading(true);
    try {
      const response = await PBancoIndexService(query);
      if (isPBancoIndexResult(response)) {
        setBancos(response.rows);
        setPagination(response.pagination);
        setResponse({
          status: 200,
          message: 'Bancos listados com sucesso',
        });
      } else {
        setBancos([]);
        setPagination(DEFAULT_PAGINATION_META);
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
  }, [setResponse]);

  return { bancos, pagination, setBancos, isLoading, fetchBancos };
};
