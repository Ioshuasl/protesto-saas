import { useState } from 'react';

import { GSistemaDeleteData } from '@/packages/administrativo/data/GSistema/GSistemaDeleteData';
import type { GSistemaInterface } from '@/packages/administrativo/interfaces/GSistema/GSistemaInterface';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGSistemaDeleteHook = () => {
  const { setResponse } = useResponse();
  const [gSistema, setGSistema] = useState<GSistemaInterface>();

  const deleteSistema = async (id: number) => {
    const response = await GSistemaDeleteData({ sistema_id: id } as GSistemaInterface);

    setGSistema({ sistema_id: id } as GSistemaInterface);

    setResponse(response);
    return response;
  };

  return { gSistema, deleteSistema };
};
