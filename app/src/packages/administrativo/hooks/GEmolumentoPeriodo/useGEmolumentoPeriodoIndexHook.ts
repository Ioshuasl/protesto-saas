import { useCallback, useState } from 'react';

import type { GEmolumentoPeriodoInterface } from '@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface';
import { GEmolumentoPeriodoIndexService } from '@/packages/administrativo/services/GEmolumentoPeriodo/GEmolumentoPeriodoIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGEmolumentoPeriodoIndexHook = () => {
  const { setResponse } = useResponse();
  const [periodos, setPeriodos] = useState<GEmolumentoPeriodoInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchPeriodos = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await GEmolumentoPeriodoIndexService();
      if (Array.isArray(response)) {
        setPeriodos(response);
        setResponse({
          status: 200,
          message: 'Periodos de emolumento listados com sucesso',
        });
      } else {
        setPeriodos([]);
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

  return { periodos, setPeriodos, isLoading, fetchPeriodos };
};
