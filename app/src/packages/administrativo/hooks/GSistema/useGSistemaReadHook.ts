import { useCallback, useState } from 'react';

import type { GSistemaInterface } from '@/packages/administrativo/interfaces/GSistema/GSistemaInterface';
import type { GSistemaIndexQuery } from '@/packages/administrativo/interfaces/GSistema/GSistemaIndexQuery';
import type { GSistemaIndexResult } from '@/packages/administrativo/interfaces/GSistema/GSistemaIndexResult';
import { GSistemaIndexService } from '@/packages/administrativo/services/GSistema/GSistemaIndexService';
import { DEFAULT_PAGINATION_META, type PaginationMeta } from '@/shared/components/pagination';
import { useResponse } from '@/shared/components/response/ResponseContext';

function isGSistemaIndexResult(value: unknown): value is GSistemaIndexResult {
  return (
    typeof value === 'object' &&
    value !== null &&
    Array.isArray((value as GSistemaIndexResult).rows) &&
    typeof (value as GSistemaIndexResult).pagination === 'object'
  );
}

export const useGSistemaReadHook = () => {
  const { setResponse } = useResponse();
  const [sistemas, setSistemas] = useState<GSistemaInterface[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta>(DEFAULT_PAGINATION_META);
  const [isLoading, setIsLoading] = useState(false);

  const fetchSistemas = useCallback(
    async (query?: GSistemaIndexQuery) => {
      setIsLoading(true);
      try {
        const response = await GSistemaIndexService(query);
        if (isGSistemaIndexResult(response)) {
          setSistemas(response.rows);
          setPagination(response.pagination);
          setResponse({
            status: 200,
            message: 'Sistemas listados com sucesso',
          });
        } else {
          setSistemas([]);
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

  return { sistemas, pagination, setSistemas, isLoading, fetchSistemas };
};
