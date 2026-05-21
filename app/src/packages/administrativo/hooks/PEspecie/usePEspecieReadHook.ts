import { useCallback, useState } from 'react';

import type { PEspecieInterface } from '@/packages/administrativo/interfaces/PEspecie/PEspecieInterface';
import type { PEspecieIndexQuery } from '@/packages/administrativo/interfaces/PEspecie/PEspecieIndexQuery';
import type { PEspecieIndexResult } from '@/packages/administrativo/interfaces/PEspecie/PEspecieIndexResult';
import { PEspecieIndexService } from '@/packages/administrativo/services/PEspecie/PEspecieIndexService';
import { DEFAULT_PAGINATION_META, type PaginationMeta } from '@/shared/components/pagination';
import { useResponse } from '@/shared/components/response/ResponseContext';

function isPEspecieIndexResult(value: unknown): value is PEspecieIndexResult {
  return (
    typeof value === 'object' &&
    value !== null &&
    Array.isArray((value as PEspecieIndexResult).rows) &&
    typeof (value as PEspecieIndexResult).pagination === 'object'
  );
}

export const usePEspecieReadHook = () => {
  const { setResponse } = useResponse();
  const [especies, setEspecies] = useState<PEspecieInterface[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta>(DEFAULT_PAGINATION_META);
  const [isLoading, setIsLoading] = useState(false);

  const fetchEspecies = useCallback(
    async (query?: PEspecieIndexQuery) => {
      setIsLoading(true);
      try {
        const response = await PEspecieIndexService(query);
        if (isPEspecieIndexResult(response)) {
          setEspecies(response.rows);
          setPagination(response.pagination);
          setResponse({
            status: 200,
            message: 'Espécies listadas com sucesso',
          });
        } else {
          setEspecies([]);
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

  return { especies, pagination, setEspecies, isLoading, fetchEspecies };
};
