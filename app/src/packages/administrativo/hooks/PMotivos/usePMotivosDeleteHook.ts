import { useState } from 'react';

import { PMotivosDeleteData } from '@/packages/administrativo/data/PMotivos/PMotivosDeleteData';
import { PMotivosInterface } from '@/packages/administrativo/interfaces/PMotivos/PMotivosInterface';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePMotivosDeleteHook = () => {
  const { setResponse } = useResponse();

  const [pMotivos, setPMotivos] = useState<PMotivosInterface>();

  const deleteMotivo = async (id: number) => {
    const response = await PMotivosDeleteData(id);

    setPMotivos({ motivos_id: id } as PMotivosInterface);

    setResponse(response);
    return response;
  };

  return { pMotivos, deleteMotivo };
};
