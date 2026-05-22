import { useCallback, useState } from 'react';

import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';
import type { PPessoaIndexQuery } from '@/packages/administrativo/interfaces/PPessoa/PPessoaIndexQuery';
import type { PPessoaIndexResult } from '@/packages/administrativo/interfaces/PPessoa/PPessoaIndexResult';
import { PPessoaIndexService } from '@/packages/administrativo/services/PPessoa/PPessoaIndexService';
import { DEFAULT_PAGINATION_META, type PaginationMeta } from '@/shared/components/pagination';
import { useResponse } from '@/shared/components/response/ResponseContext';

function isPPessoaIndexResult(value: unknown): value is PPessoaIndexResult {
  return (
    typeof value === 'object' &&
    value !== null &&
    Array.isArray((value as PPessoaIndexResult).rows) &&
    typeof (value as PPessoaIndexResult).pagination === 'object'
  );
}

export const usePPessoaReadHook = () => {
  const { setResponse } = useResponse();
  const [pessoas, setPessoas] = useState<PPessoaInterface[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta>(DEFAULT_PAGINATION_META);
  const [isLoading, setIsLoading] = useState(false);

  const fetchPessoas = useCallback(
    async (query?: PPessoaIndexQuery) => {
      setIsLoading(true);
      try {
        const response = await PPessoaIndexService(query);
        if (isPPessoaIndexResult(response)) {
          setPessoas(response.rows);
          setPagination(response.pagination);
          setResponse({
            status: 200,
            message: 'Pessoas listadas com sucesso',
          });
        } else {
          setPessoas([]);
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

  return { pessoas, pagination, setPessoas, isLoading, fetchPessoas };
};
