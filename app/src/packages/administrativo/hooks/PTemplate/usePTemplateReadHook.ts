import { useCallback, useState } from 'react';

import type { PTemplateIndexQuery } from '@/packages/administrativo/interfaces/PTemplate/PTemplateIndexQuery';
import type { PTemplateIndexResult } from '@/packages/administrativo/interfaces/PTemplate/PTemplateIndexResult';
import type { PTemplateInterface } from '@/packages/administrativo/interfaces/PTemplate/PTemplateInterface';
import { PTemplateIndexService } from '@/packages/administrativo/services/PTemplate/PTemplateIndexService';
import { DEFAULT_PAGINATION_META, type PaginationMeta } from '@/shared/components/pagination';
import { useResponse } from '@/shared/components/response/ResponseContext';

function isPTemplateIndexResult(value: unknown): value is PTemplateIndexResult {
  return (
    typeof value === 'object' &&
    value !== null &&
    Array.isArray((value as PTemplateIndexResult).rows) &&
    typeof (value as PTemplateIndexResult).pagination === 'object'
  );
}

export const usePTemplateReadHook = () => {
  const { setResponse } = useResponse();
  const [templates, setTemplates] = useState<PTemplateInterface[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta>(DEFAULT_PAGINATION_META);
  const [isLoading, setIsLoading] = useState(false);

  const fetchTemplates = useCallback(
    async (query?: PTemplateIndexQuery) => {
      setIsLoading(true);
      try {
        const response = await PTemplateIndexService(query);
        if (isPTemplateIndexResult(response)) {
          setTemplates(response.rows);
          setPagination(response.pagination);
          setResponse({
            status: 200,
            message: 'Templates listados com sucesso',
          });
        } else {
          setTemplates([]);
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

  return { templates, pagination, setTemplates, isLoading, fetchTemplates };
};
