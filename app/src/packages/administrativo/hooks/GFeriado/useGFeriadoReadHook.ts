import { useCallback, useState } from 'react';

import type { GFeriadoInterface } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface';
import { GFeriadoIndexService } from '@/packages/administrativo/services/GFeriado/GFeriadoIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGFeriadoReadHook = () => {
  const { setResponse } = useResponse();
  const [feriados, setFeriados] = useState<GFeriadoInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchFeriados = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await GFeriadoIndexService();
      if (Array.isArray(response)) {
        setFeriados(response);
        setResponse({
          status: 200,
          message: 'Feriados listados com sucesso',
        });
      } else {
        setFeriados([]);
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

  return { feriados, setFeriados, isLoading, fetchFeriados };
};
