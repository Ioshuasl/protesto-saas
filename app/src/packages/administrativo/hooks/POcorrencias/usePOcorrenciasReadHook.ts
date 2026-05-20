import { useCallback, useState } from 'react';

import type { POcorrenciasInterface } from '@/packages/administrativo/interfaces/POcorrencias/POcorrenciasInterface';
import { POcorrenciasIndexService } from '@/packages/administrativo/services/POcorrencias/POcorrenciasIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePOcorrenciasReadHook = () => {
  const { setResponse } = useResponse();
  const [ocorrencias, setOcorrencias] = useState<POcorrenciasInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchOcorrencias = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await POcorrenciasIndexService();
      if (Array.isArray(response)) {
        setOcorrencias(response);
        setResponse({
          status: 200,
          message: 'Ocorrências listadas com sucesso',
        });
      } else {
        setOcorrencias([]);
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

  return { ocorrencias, setOcorrencias, isLoading, fetchOcorrencias };
};
