import { useState } from 'react';

import type { PTituloApontarInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloApontarInterface';
import { isTituloListItem, type TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { PTituloApontarService } from '@/packages/administrativo/services/PTitulo/PTituloApontarService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloApontarHook = () => {
  const { setResponse } = useResponse();
  const [pTitulo, setPTitulo] = useState<TituloListItem | null>(null);

  const apontarTitulo = async (id: number, payload: PTituloApontarInterface) => {
    const response = await PTituloApontarService(id, payload);

    if (isTituloListItem(response)) {
      setPTitulo(response);
      setResponse({ status: 200, message: 'Título apontado com sucesso' });
    } else {
      setResponse(response);
    }

    return response;
  };

  return { pTitulo, apontarTitulo };
};
