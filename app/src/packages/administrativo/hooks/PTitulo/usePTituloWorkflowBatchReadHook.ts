import { useCallback, useState } from 'react';
import type { PTituloBatchRowBase } from '@/packages/administrativo/data/PTitulo/ptituloIndexItemToBatchMapper';
import { PTituloWorkflowBatchIndexService } from '@/packages/administrativo/services/PTitulo/PTituloWorkflowBatchIndexService';
import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import { useResponse } from '@/shared/components/response/ResponseContext';

type PTituloWorkflowBatchReadHookConfig = {
  successMessage: string;
};

export function usePTituloWorkflowBatchReadHook(config: PTituloWorkflowBatchReadHookConfig) {
  const { setResponse } = useResponse();
  const [titulos, setTitulos] = useState<PTituloBatchRowBase[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchTitulos = useCallback(
    async (query?: PTituloIndexQuery) => {
      setIsLoading(true);
      try {
        const response = await PTituloWorkflowBatchIndexService(query);

        if (Array.isArray(response)) {
          setTitulos(response);
          setResponse({
            status: 200,
            message: config.successMessage,
          });
        } else {
          setTitulos([]);
          setResponse({
            status: (response as { status?: number }).status,
            message: (response as { message?: string }).message,
            error: (response as { message?: string }).message,
          });
        }

        return response;
      } finally {
        setIsLoading(false);
      }
    },
    [config.successMessage, setResponse],
  );

  return { titulos, setTitulos, isLoading, fetchTitulos };
}
