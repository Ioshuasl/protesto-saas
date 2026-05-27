'use client';

import { useCallback, useState } from 'react';

import type { GEmolumentoItemInterface } from '@/packages/administrativo/interfaces/GEmolumentoItem/GEmolumentoItemInterface';
import { GEmolumentoItemIndexService } from '@/packages/administrativo/services/GEmolumentoItem/GEmolumentoItemIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGEmolumentoItemIndexHook = () => {
  const { setResponse } = useResponse();
  const [itens, setItens] = useState<GEmolumentoItemInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchItens = useCallback(
    async (emolumentoId: number, emolumentoPeriodoId: number) => {
      setIsLoading(true);
      try {
        const response = await GEmolumentoItemIndexService(emolumentoId, emolumentoPeriodoId);
        if (Array.isArray(response)) {
          setItens(response);
          setResponse({
            status: 200,
            message: 'Itens de emolumento listados com sucesso',
          });
        } else {
          setItens([]);
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

  return { itens, setItens, isLoading, fetchItens };
};
