import { useCallback, useState } from 'react';

import type { GFeriadoInterface } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface';
import type { GFeriadoIndexQuery } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoIndexQuery';
import type { GFeriadoIndexResult } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoIndexResult';
import { GFeriadoIndexService } from '@/packages/administrativo/services/GFeriado/GFeriadoIndexService';
import { DEFAULT_PAGINATION_META, type PaginationMeta } from '@/shared/components/pagination';
import { useResponse } from '@/shared/components/response/ResponseContext';

function isGFeriadoIndexResult(value: unknown): value is GFeriadoIndexResult {
  return (
    typeof value === 'object' &&
    value !== null &&
    Array.isArray((value as GFeriadoIndexResult).rows) &&
    typeof (value as GFeriadoIndexResult).pagination === 'object'
  );
}

export const useGFeriadoReadHook = () => {
  const { setResponse } = useResponse();
  const [feriados, setFeriados] = useState<GFeriadoInterface[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta>(DEFAULT_PAGINATION_META);
  const [isLoading, setIsLoading] = useState(false);

  const fetchFeriados = useCallback(async (query?: GFeriadoIndexQuery) => {
    setIsLoading(true);
    try {
      const response = await GFeriadoIndexService(query);
      if (isGFeriadoIndexResult(response)) {
        setFeriados(response.rows);
        setPagination(response.pagination);
        setResponse({
          status: 200,
          message: 'Feriados listados com sucesso',
        });
      } else {
        setFeriados([]);
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

  return { feriados, pagination, setFeriados, isLoading, fetchFeriados };
};
