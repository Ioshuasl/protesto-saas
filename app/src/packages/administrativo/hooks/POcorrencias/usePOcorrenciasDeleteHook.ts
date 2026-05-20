import { useState } from 'react';

import { POcorrenciasDeleteData } from '@/packages/administrativo/data/POcorrencias/POcorrenciasDeleteData';
import type { POcorrenciasInterface } from '@/packages/administrativo/interfaces/POcorrencias/POcorrenciasInterface';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePOcorrenciasDeleteHook = () => {
  const { setResponse } = useResponse();

  const [pOcorrencias, setPOcorrencias] = useState<POcorrenciasInterface>();

  const deleteOcorrencia = async (id: number) => {
    const response = await POcorrenciasDeleteData(id);

    setPOcorrencias({ ocorrencias_id: id } as POcorrenciasInterface);

    setResponse(response);
    return response;
  };

  return { pOcorrencias, deleteOcorrencia };
};
