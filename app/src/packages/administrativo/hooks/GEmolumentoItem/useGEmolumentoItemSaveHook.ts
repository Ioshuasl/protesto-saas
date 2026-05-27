'use client';

import { useState } from 'react';

import type { GEmolumentoItemInterface } from '@/packages/administrativo/interfaces/GEmolumentoItem/GEmolumentoItemInterface';
import { GEmolumentoItemSaveService } from '@/packages/administrativo/services/GEmolumentoItem/GEmolumentoItemSaveService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGEmolumentoItemSaveHook = () => {
  const { setResponse } = useResponse();
  const [item, setItem] = useState<GEmolumentoItemInterface | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const saveItem = async (data: Omit<GEmolumentoItemInterface, 'emolumento_item_id'>) => {
    const response = await GEmolumentoItemSaveService(data);

    if (response && typeof response === 'object' && 'emolumento_item_id' in response) {
      setItem(response as GEmolumentoItemInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'emolumento_item_id' in response
        ? {
            status: 201,
            message: 'Item de emolumento criado com sucesso',
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

  return { item, setItem, saveItem, isOpen, setIsOpen };
};
