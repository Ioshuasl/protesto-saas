import { useState } from 'react';

import type { GEmolumentoInterface } from '@/packages/administrativo/interfaces/GEmolumento/GEmolumentoInterface';
import { GEmolumentoSaveCreateService } from '@/packages/administrativo/services/GEmolumento/GEmolumentoSaveCreateService';
import { GEmolumentoSaveUpdateService } from '@/packages/administrativo/services/GEmolumento/GEmolumentoSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGEmolumentoSaveHook = () => {
  const { setResponse } = useResponse();
  const [gEmolumento, setGEmolumento] = useState<GEmolumentoInterface | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const saveEmolumento = async (
    data: Omit<GEmolumentoInterface, 'emolumento_id'> | Partial<GEmolumentoInterface>,
    selected: GEmolumentoInterface | null,
  ) => {
    const response = selected
      ? await GEmolumentoSaveUpdateService(selected.emolumento_id, data)
      : await GEmolumentoSaveCreateService(data as Omit<GEmolumentoInterface, 'emolumento_id'>);

    if (response && typeof response === 'object' && 'emolumento_id' in response) {
      setGEmolumento(response as GEmolumentoInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'emolumento_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected ? 'Emolumento atualizado com sucesso' : 'Emolumento criado com sucesso',
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

  return { gEmolumento, saveEmolumento, isOpen, setIsOpen };
};
