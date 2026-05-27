'use client';

import { useState } from 'react';

import type { GEmolumentoItemInterface } from '@/packages/administrativo/interfaces/GEmolumentoItem/GEmolumentoItemInterface';
import { GEmolumentoItemUpdateService } from '@/packages/administrativo/services/GEmolumentoItem/GEmolumentoItemUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGEmolumentoItemUpdateHook = () => {
  const { setResponse } = useResponse();
  const [item, setItem] = useState<GEmolumentoItemInterface | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const updateItem = async (id: number, data: Partial<GEmolumentoItemInterface>) => {
    const response = await GEmolumentoItemUpdateService(id, data);

    if (response && typeof response === 'object' && 'emolumento_item_id' in response) {
      setItem(response as GEmolumentoItemInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'emolumento_item_id' in response
        ? {
            status: 200,
            message: 'Item de emolumento atualizado com sucesso',
          }
        : {
            status: (response as { status?: number }).status,
            message: (response as { message?: string }).message,
            error: (response as { message?: string }).message,
          },
    );

    setIsOpen(false);
    return response;
  };

  return { item, setItem, updateItem, isOpen, setIsOpen };
};
