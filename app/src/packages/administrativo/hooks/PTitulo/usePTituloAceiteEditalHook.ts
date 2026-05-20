import { useState } from 'react';

import type { PTituloAceiteEditalInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloAceiteEditalInterface';
import { isTituloListItem, type TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { PTituloAceiteEditalService } from '@/packages/administrativo/services/PTitulo/PTituloAceiteEditalService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloAceiteEditalHook = () => {
  const { setResponse } = useResponse();
  const [pTitulo, setPTitulo] = useState<TituloListItem | null>(null);

  const aceiteEdital = async (id: number, payload: PTituloAceiteEditalInterface) => {
    const response = await PTituloAceiteEditalService(id, payload);

    if (isTituloListItem(response)) {
      setPTitulo(response);
      setResponse({ status: 200, message: 'Aceite/Edital aplicado com sucesso' });
    } else {
      setResponse(response);
    }

    return response;
  };

  return { pTitulo, aceiteEdital };
};
