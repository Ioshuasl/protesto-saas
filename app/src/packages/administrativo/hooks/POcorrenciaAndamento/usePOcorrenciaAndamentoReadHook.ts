import { useCallback, useState } from 'react';

import type { POcorrenciaAndamentoInterface } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface';
import type { POcorrenciaAndamentoIndexQuery } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoIndexQuery';
import type { POcorrenciaAndamentoIndexResult } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoIndexResult';
import { POcorrenciaAndamentoIndexService } from '@/packages/administrativo/services/POcorrenciaAndamento/POcorrenciaAndamentoIndexService';
import { DEFAULT_PAGINATION_META, type PaginationMeta } from '@/shared/components/pagination';
import { useResponse } from '@/shared/components/response/ResponseContext';

function isPOcorrenciaAndamentoIndexResult(
  value: unknown,
): value is POcorrenciaAndamentoIndexResult {
  return (
    typeof value === 'object' &&
    value !== null &&
    Array.isArray((value as POcorrenciaAndamentoIndexResult).rows) &&
    typeof (value as POcorrenciaAndamentoIndexResult).pagination === 'object'
  );
}

export const usePOcorrenciaAndamentoReadHook = () => {
  const { setResponse } = useResponse();
  const [ocorrenciasAndamento, setOcorrenciasAndamento] = useState<
    POcorrenciaAndamentoInterface[]
  >([]);
  const [pagination, setPagination] = useState<PaginationMeta>(DEFAULT_PAGINATION_META);
  const [isLoading, setIsLoading] = useState(false);

  const fetchOcorrenciasAndamento = useCallback(
    async (query?: POcorrenciaAndamentoIndexQuery) => {
      setIsLoading(true);
      try {
        const response = await POcorrenciaAndamentoIndexService(query);
        if (isPOcorrenciaAndamentoIndexResult(response)) {
          setOcorrenciasAndamento(response.rows);
          setPagination(response.pagination);
          setResponse({
            status: 200,
            message: 'Ocorrências de andamento listadas com sucesso',
          });
        } else {
          setOcorrenciasAndamento([]);
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

  return {
    ocorrenciasAndamento,
    pagination,
    setOcorrenciasAndamento,
    isLoading,
    fetchOcorrenciasAndamento,
  };
};
