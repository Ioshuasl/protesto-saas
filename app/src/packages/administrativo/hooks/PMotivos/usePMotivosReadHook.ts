import { useCallback, useState } from 'react';

import { PMotivosInterface } from '@/packages/administrativo/interfaces/PMotivos/PMotivosInterface';
import type { PMotivosIndexQuery } from '@/packages/administrativo/interfaces/PMotivos/PMotivosIndexQuery';
import { PMotivosIndexService } from '@/packages/administrativo/services/PMotivos/PMotivosIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePMotivosReadHook = () => {
  const { setResponse } = useResponse();
  const [motivos, setMotivos] = useState<PMotivosInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchMotivos = useCallback(async (query?: PMotivosIndexQuery) => {
    setIsLoading(true);
    try {
      const response = await PMotivosIndexService(query);
      if (Array.isArray(response)) {
        setMotivos(response);
        setResponse({
          status: 200,
          message: 'Motivos listados com sucesso',
        });
      } else {
        setMotivos([]);
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

  return { motivos, setMotivos, isLoading, fetchMotivos };
};
