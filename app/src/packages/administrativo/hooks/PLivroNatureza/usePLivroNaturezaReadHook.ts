import { useCallback, useState } from 'react';

import type { PLivroNaturezaInterface } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface';
import type { PLivroNaturezaIndexQuery } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaIndexQuery';
import type { PLivroNaturezaIndexResult } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaIndexResult';
import { PLivroNaturezaIndexService } from '@/packages/administrativo/services/PLivroNatureza/PLivroNaturezaIndexService';
import { DEFAULT_PAGINATION_META, type PaginationMeta } from '@/shared/components/pagination';
import { useResponse } from '@/shared/components/response/ResponseContext';

function isPLivroNaturezaIndexResult(value: unknown): value is PLivroNaturezaIndexResult {
  return (
    typeof value === 'object' &&
    value !== null &&
    Array.isArray((value as PLivroNaturezaIndexResult).rows) &&
    typeof (value as PLivroNaturezaIndexResult).pagination === 'object'
  );
}

export const usePLivroNaturezaReadHook = () => {
  const { setResponse } = useResponse();
  const [naturezas, setNaturezas] = useState<PLivroNaturezaInterface[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta>(DEFAULT_PAGINATION_META);
  const [isLoading, setIsLoading] = useState(false);

  const fetchNaturezas = useCallback(
    async (query?: PLivroNaturezaIndexQuery) => {
      setIsLoading(true);
      try {
        const response = await PLivroNaturezaIndexService(query);
        if (isPLivroNaturezaIndexResult(response)) {
          setNaturezas(response.rows);
          setPagination(response.pagination);
          setResponse({
            status: 200,
            message: 'Naturezas de livro listadas com sucesso',
          });
        } else {
          setNaturezas([]);
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
    },
    [setResponse],
  );

  return { naturezas, pagination, setNaturezas, isLoading, fetchNaturezas };
};
