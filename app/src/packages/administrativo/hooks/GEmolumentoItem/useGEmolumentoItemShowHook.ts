'use client';

import { useState } from 'react';

import type { GEmolumentoItemInterface } from '@/packages/administrativo/interfaces/GEmolumentoItem/GEmolumentoItemInterface';
import { GEmolumentoItemShowService } from '@/packages/administrativo/services/GEmolumentoItem/GEmolumentoItemShowService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGEmolumentoItemShowHook = () => {
  const { setResponse } = useResponse();
  const [item, setItem] = useState<GEmolumentoItemInterface | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchItem = async (id: number) => {
    setIsLoading(true);
    try {
      const response = await GEmolumentoItemShowService(id);
      if (response && typeof response === 'object' && 'emolumento_item_id' in response) {
        setItem(response as GEmolumentoItemInterface);
        setResponse({
          status: 200,
          message: 'Item de emolumento carregado com sucesso',
        });
      } else {
        setItem(null);
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

  return { item, setItem, isLoading, fetchItem };
};
