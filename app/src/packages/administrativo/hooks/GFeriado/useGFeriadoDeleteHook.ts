import { useState } from 'react';

import { GFeriadoDeleteData } from '@/packages/administrativo/data/GFeriado/GFeriadoDeleteData';
import type { GFeriadoInterface } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGFeriadoDeleteHook = () => {
  const { setResponse } = useResponse();

  const [gFeriado, setGFeriado] = useState<GFeriadoInterface>();

  const deleteFeriado = async (id: number) => {
    const response = await GFeriadoDeleteData({ feriado_id: id } as GFeriadoInterface);

    setGFeriado({ feriado_id: id } as GFeriadoInterface);

    setResponse(response);
    return response;
  };

  return { gFeriado, deleteFeriado };
};
