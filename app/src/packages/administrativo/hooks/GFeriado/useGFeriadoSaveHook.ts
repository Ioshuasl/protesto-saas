import { useState } from 'react';

import type { GFeriadoInterface } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface';
import { FeriadoFormValues } from '@/packages/administrativo/schemas/GFeriado/GFeriadoFormSchema';
import { GFeriadoSaveCreateService } from '@/packages/administrativo/services/GFeriado/GFeriadoSaveCreateService';
import { GFeriadoSaveUpdateService } from '@/packages/administrativo/services/GFeriado/GFeriadoSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export type FeriadoSavePayload = FeriadoFormValues & { dia: number; mes: number; ano: number };

export const useGFeriadoSaveHook = () => {
  const { setResponse } = useResponse();
  const [gFeriado, setGFeriado] = useState<GFeriadoInterface | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const saveFeriado = async (data: FeriadoSavePayload, selected: GFeriadoInterface | null) => {
    const payload = {
      ...data,
      data: data.data.toISOString(),
    };
    const response = selected
      ? await GFeriadoSaveUpdateService(selected.feriado_id, payload as Partial<GFeriadoInterface>)
      : await GFeriadoSaveCreateService(payload as Omit<GFeriadoInterface, 'feriado_id'>);

    if (response && typeof response === 'object' && 'feriado_id' in response) {
      setGFeriado(response as GFeriadoInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'feriado_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected ? 'Feriado atualizado com sucesso' : 'Feriado criado com sucesso',
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

  return { gFeriado, saveFeriado };
};
