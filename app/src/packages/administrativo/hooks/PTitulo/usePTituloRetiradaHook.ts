import { useState } from 'react';

import { isTituloListItem, type TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import type { PTituloRetiradaFormInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloRetiradaFormInterface';
import { PTituloRetiradaService } from '@/packages/administrativo/services/PTitulo/PTituloRetiradaService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloRetiradaHook = () => {
  const { setResponse } = useResponse();
  const [pTitulo, setPTitulo] = useState<TituloListItem | null>(null);

  const retiradaTitulo = async (id: number, payload: PTituloRetiradaFormInterface) => {
    const response = await PTituloRetiradaService(id, payload);

    if (isTituloListItem(response)) {
      setPTitulo(response);
      setResponse({ status: 200, message: 'Retirada do título registrada com sucesso' });
    } else {
      setResponse(response);
    }

    return response;
  };

  return { pTitulo, retiradaTitulo };
};
