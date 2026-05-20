import { useState } from 'react';

import type { PTituloLiquidacaoFormInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloLiquidacaoFormInterface';
import { isTituloListItem, type TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { PTituloLiquidacaoService } from '@/packages/administrativo/services/PTitulo/PTituloLiquidacaoService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloLiquidacaoHook = () => {
  const { setResponse } = useResponse();
  const [pTitulo, setPTitulo] = useState<TituloListItem | null>(null);

  const liquidarTitulo = async (id: number, payload?: PTituloLiquidacaoFormInterface) => {
    const response = await PTituloLiquidacaoService(id, payload);

    if (isTituloListItem(response)) {
      setPTitulo(response);
      setResponse({ status: 200, message: 'Título liquidado com sucesso' });
    } else {
      setResponse(response);
    }

    return response;
  };

  return { pTitulo, liquidarTitulo };
};
