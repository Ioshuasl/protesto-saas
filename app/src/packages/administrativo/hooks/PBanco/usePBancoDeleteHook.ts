import { useState } from 'react';

import { PBancoDeleteData } from '@/packages/administrativo/data/PBanco/PBancoDeleteData';
import { PBancoInterface } from '@/packages/administrativo/interfaces/PBanco/PBancoInterface';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePBancoDeleteHook = () => {
  const { setResponse } = useResponse();

  const [pBanco, setPBanco] = useState<PBancoInterface>();

  const deleteBanco = async (id: number) => {
    const response = await PBancoDeleteData(id);

    setPBanco({ banco_id: id } as PBancoInterface);

    setResponse(response);
    return response;
  };

  return { pBanco, deleteBanco };
};
