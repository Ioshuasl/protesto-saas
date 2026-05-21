import { useCallback, useState } from 'react';

import type { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import type { PLivroAndamentoIndexQuery } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoIndexQuery';
import type { PLivroAndamentoIndexResult } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoIndexResult';
import { PLivroAndamentoIndexService } from '@/packages/administrativo/services/PLivroAndamento/PLivroAndamentoIndexService';
import { DEFAULT_PAGINATION_META, type PaginationMeta } from '@/shared/components/pagination';
import { useResponse } from '@/shared/components/response/ResponseContext';

function isPLivroAndamentoIndexResult(value: unknown): value is PLivroAndamentoIndexResult {
  return (
    typeof value === 'object' &&
    value !== null &&
    Array.isArray((value as PLivroAndamentoIndexResult).rows) &&
    typeof (value as PLivroAndamentoIndexResult).pagination === 'object'
  );
}

export const usePLivroAndamentoReadHook = () => {
  const { setResponse } = useResponse();
  const [livrosAndamento, setLivrosAndamento] = useState<PLivroAndamentoInterface[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta>(DEFAULT_PAGINATION_META);
  const [isLoading, setIsLoading] = useState(false);

  const fetchLivrosAndamento = useCallback(
    async (query?: PLivroAndamentoIndexQuery) => {
      setIsLoading(true);
      try {
        const response = await PLivroAndamentoIndexService(query);
        if (isPLivroAndamentoIndexResult(response)) {
          setLivrosAndamento(response.rows);
          setPagination(response.pagination);
          setResponse({
            status: 200,
            message: 'Livros em andamento listados com sucesso',
          });
        } else {
          setLivrosAndamento([]);
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

  return { livrosAndamento, pagination, setLivrosAndamento, isLoading, fetchLivrosAndamento };
};
