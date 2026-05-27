'use client';

import { useCallback, useState } from 'react';

import type { TabelionatoProtestoDashboardFunilItem } from '@/packages/administrativo/interfaces/TabelionatoProtestoDashboard/TabelionatoProtestoDashboardFunilItem';
import { TabelionatoProtestoDashboardFunilService } from '@/packages/administrativo/services/TabelionatoProtestoDashboard/TabelionatoProtestoDashboardFunilService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useTabelionatoProtestoDashboardFunilHook = () => {
  const { setResponse } = useResponse();
  const [funil, setFunil] = useState<TabelionatoProtestoDashboardFunilItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchFunil = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await TabelionatoProtestoDashboardFunilService();
      if (Array.isArray(response)) {
        setFunil(response);
        setResponse({
          status: 200,
          message: 'Funil do dashboard carregado com sucesso',
        });
      } else {
        setFunil([]);
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

  return { funil, setFunil, isLoading, fetchFunil };
};
