import { useCallback, useState } from 'react';

import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import type { PTituloIndexResult } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexResult';
import type { TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { DEFAULT_PAGINATION_META, type PaginationMeta } from '@/shared/components/pagination';
import { useResponse } from '@/shared/components/response/ResponseContext';

function isPTituloIndexResult(value: unknown): value is PTituloIndexResult {
  return (
    typeof value === 'object' &&
    value !== null &&
    Array.isArray((value as PTituloIndexResult).rows) &&
    typeof (value as PTituloIndexResult).pagination === 'object'
  );
}

type PTituloSomenteIndexServiceFn = (
  query?: PTituloIndexQuery,
) => Promise<PTituloIndexResult | { status: number; message: string }>;

export function createPTituloSomenteReadHook(
  service: PTituloSomenteIndexServiceFn,
  successMessage: string,
) {
  return function usePTituloSomenteReadHook() {
    const { setResponse } = useResponse();
    const [titulos, setTitulos] = useState<TituloListItem[]>([]);
    const [pagination, setPagination] = useState<PaginationMeta>(DEFAULT_PAGINATION_META);
    const [isLoading, setIsLoading] = useState(false);

    const fetchTitulos = useCallback(
      async (query?: PTituloIndexQuery) => {
        setIsLoading(true);
        try {
          const response = await service(query);
          if (isPTituloIndexResult(response)) {
            setTitulos(response.rows);
            setPagination(response.pagination);
            setResponse({
              status: 200,
              message: successMessage,
            });
          } else {
            setTitulos([]);
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

    return { titulos, pagination, setTitulos, isLoading, fetchTitulos };
  };
}
