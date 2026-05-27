import { useState } from 'react';

import type { GEmolumentoPeriodoInterface } from '@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface';
import { GEmolumentoPeriodoShowService } from '@/packages/administrativo/services/GEmolumentoPeriodo/GEmolumentoPeriodoShowService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGEmolumentoPeriodoShowHook = () => {
  const { setResponse } = useResponse();
  const [periodo, setPeriodo] = useState<GEmolumentoPeriodoInterface | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchPeriodo = async (id: number) => {
    setIsLoading(true);
    try {
      const response = await GEmolumentoPeriodoShowService(id);
      if (response && typeof response === 'object' && 'emolumento_periodo_id' in response) {
        setPeriodo(response as GEmolumentoPeriodoInterface);
        setResponse({
          status: 200,
          message: 'Periodo de emolumento carregado com sucesso',
        });
      } else {
        setPeriodo(null);
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
  };

  return { periodo, setPeriodo, isLoading, fetchPeriodo };
};
