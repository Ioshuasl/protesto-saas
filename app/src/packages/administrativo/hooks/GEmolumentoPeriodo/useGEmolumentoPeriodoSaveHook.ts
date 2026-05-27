import { useState } from 'react';

import type { GEmolumentoPeriodoInterface } from '@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface';
import { GEmolumentoPeriodoSaveCreateService } from '@/packages/administrativo/services/GEmolumentoPeriodo/GEmolumentoPeriodoSaveCreateService';
import { GEmolumentoPeriodoSaveUpdateService } from '@/packages/administrativo/services/GEmolumentoPeriodo/GEmolumentoPeriodoSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGEmolumentoPeriodoSaveHook = () => {
  const { setResponse } = useResponse();
  const [periodo, setPeriodo] = useState<GEmolumentoPeriodoInterface | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const savePeriodo = async (
    data:
      | Omit<GEmolumentoPeriodoInterface, 'emolumento_periodo_id'>
      | Partial<GEmolumentoPeriodoInterface>,
    selected: GEmolumentoPeriodoInterface | null,
  ) => {
    const response = selected
      ? await GEmolumentoPeriodoSaveUpdateService(selected.emolumento_periodo_id, data)
      : await GEmolumentoPeriodoSaveCreateService(
          data as Omit<GEmolumentoPeriodoInterface, 'emolumento_periodo_id'>,
        );

    if (response && typeof response === 'object' && 'emolumento_periodo_id' in response) {
      setPeriodo(response as GEmolumentoPeriodoInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'emolumento_periodo_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected
              ? 'Periodo de emolumento atualizado com sucesso'
              : 'Periodo de emolumento criado com sucesso',
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

  return { periodo, savePeriodo, isOpen, setIsOpen };
};
