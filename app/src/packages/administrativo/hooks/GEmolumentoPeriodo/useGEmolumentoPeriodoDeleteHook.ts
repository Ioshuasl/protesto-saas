import { useState } from 'react';

import type { GEmolumentoPeriodoInterface } from '@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface';
import { GEmolumentoPeriodoDeleteService } from '@/packages/administrativo/services/GEmolumentoPeriodo/GEmolumentoPeriodoDeleteService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGEmolumentoPeriodoDeleteHook = () => {
  const { setResponse } = useResponse();

  const [periodo, setPeriodo] = useState<GEmolumentoPeriodoInterface>();

  const deletePeriodo = async (id: number) => {
    const response = await GEmolumentoPeriodoDeleteService({
      emolumento_periodo_id: id,
    } as GEmolumentoPeriodoInterface);

    setPeriodo({ emolumento_periodo_id: id } as GEmolumentoPeriodoInterface);

    setResponse(response);
    return response;
  };

  return { periodo, deletePeriodo };
};
