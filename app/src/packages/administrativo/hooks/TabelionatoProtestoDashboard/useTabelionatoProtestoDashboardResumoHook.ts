'use client';

import { useCallback, useState } from 'react';

import type { TabelionatoProtestoDashboardResumo } from '@/packages/administrativo/interfaces/TabelionatoProtestoDashboard/TabelionatoProtestoDashboardResumo';
import { TabelionatoProtestoDashboardResumoService } from '@/packages/administrativo/services/TabelionatoProtestoDashboard/TabelionatoProtestoDashboardResumoService';
import { useResponse } from '@/shared/components/response/ResponseContext';

function isResumoPayload(value: unknown): value is TabelionatoProtestoDashboardResumo {
  return typeof value === 'object' && value !== null && 'total_titulos' in value;
}

export const useTabelionatoProtestoDashboardResumoHook = () => {
  const { setResponse } = useResponse();
  const [resumo, setResumo] = useState<TabelionatoProtestoDashboardResumo | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchResumo = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await TabelionatoProtestoDashboardResumoService();
      if (isResumoPayload(response)) {
        setResumo(response);
        setResponse({
          status: 200,
          message: 'Resumo do dashboard carregado com sucesso',
        });
      } else {
        setResumo(null);
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

  return { resumo, setResumo, isLoading, fetchResumo };
};
