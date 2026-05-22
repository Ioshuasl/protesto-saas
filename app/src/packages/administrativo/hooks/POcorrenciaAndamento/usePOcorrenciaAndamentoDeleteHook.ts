import { useState } from 'react';

import { POcorrenciaAndamentoDeleteData } from '@/packages/administrativo/data/POcorrenciaAndamento/POcorrenciaAndamentoDeleteData';
import type { POcorrenciaAndamentoInterface } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePOcorrenciaAndamentoDeleteHook = () => {
  const { setResponse } = useResponse();

  const [pOcorrenciaAndamento, setPOcorrenciaAndamento] =
    useState<POcorrenciaAndamentoInterface>();

  const deleteOcorrenciaAndamento = async (id: number) => {
    const response = await POcorrenciaAndamentoDeleteData(id);

    setPOcorrenciaAndamento({ ocorrencia_andamento_id: id } as POcorrenciaAndamentoInterface);

    setResponse(response);
    return response;
  };

  return { pOcorrenciaAndamento, deleteOcorrenciaAndamento };
};
