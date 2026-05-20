import { useState } from 'react';

import { PEspecieDeleteData } from '@/packages/administrativo/data/PEspecie/PEspecieDeleteData';
import { PEspecieInterface } from '@/packages/administrativo/interfaces/PEspecie/PEspecieInterface';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePEspecieDeleteHook = () => {
  const { setResponse } = useResponse();

  const [pEspecie, setPEspecie] = useState<PEspecieInterface>();

  const deleteEspecie = async (id: number) => {
    const response = await PEspecieDeleteData(id);

    setPEspecie({ especie_id: id } as PEspecieInterface);

    setResponse(response);
    return response;
  };

  return { pEspecie, deleteEspecie };
};
