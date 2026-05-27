'use client';

import { useCallback, useState } from 'react';

import type {
  GEmolumentoListInterface,
  GEmolumentoListQuery,
  GEmolumentoListResult,
} from '@/packages/administrativo/interfaces/GEmolumentoList/GEmolumentoListInterface';
import { GEmolumentoListService } from '@/packages/administrativo/services/GEmolumentoList/GEmolumentoListService';
import { DEFAULT_PAGINATION_META, type PaginationMeta } from '@/shared/components/pagination';
import { useResponse } from '@/shared/components/response/ResponseContext';

function isGEmolumentoListResult(value: unknown): value is GEmolumentoListResult {
  return (
    typeof value === 'object' &&
    value !== null &&
    Array.isArray((value as GEmolumentoListResult).rows) &&
    typeof (value as GEmolumentoListResult).pagination === 'object'
  );
}

export const useGEmolumentoListHook = () => {
  const { setResponse } = useResponse();
  const [itens, setItens] = useState<GEmolumentoListInterface[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta>(DEFAULT_PAGINATION_META);
  const [isLoading, setIsLoading] = useState(false);

  const fetchItens = useCallback(
    async (query?: GEmolumentoListQuery) => {
      setIsLoading(true);
      try {
        const response = await GEmolumentoListService(query);
        if (isGEmolumentoListResult(response)) {
          setItens(response.rows);
          setPagination(response.pagination);
          setResponse({
            status: 200,
            message: 'Lista detalhada de emolumentos carregada com sucesso',
          });
        } else {
          setItens([]);
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

  return { itens, pagination, setItens, isLoading, fetchItens };
};
