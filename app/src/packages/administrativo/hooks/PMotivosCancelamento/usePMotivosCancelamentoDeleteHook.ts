import { useState } from 'react';

import { PMotivosCancelamentoDeleteData } from '@/packages/administrativo/data/PMotivosCancelamento/PMotivosCancelamentoDeleteData';
import type { PMotivosCancelamentoInterface } from '@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoInterface';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePMotivosCancelamentoDeleteHook = () => {
  const { setResponse } = useResponse();

  const [pMotivosCancelamento, setPMotivosCancelamento] = useState<PMotivosCancelamentoInterface>();

  const deleteMotivoCancelamento = async (id: number) => {
    const response = await PMotivosCancelamentoDeleteData(id);

    setPMotivosCancelamento({ motivos_cancelamento_id: id } as PMotivosCancelamentoInterface);

    setResponse(response);
    return response;
  };

  return { pMotivosCancelamento, deleteMotivoCancelamento };
};
