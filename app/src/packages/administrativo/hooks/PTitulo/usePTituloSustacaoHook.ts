import { useState } from 'react';

import { isTituloListItem, type TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import type { PTituloSustacaoFormInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloSustacaoFormInterface';
import { PTituloSustacaoService } from '@/packages/administrativo/services/PTitulo/PTituloSustacaoService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloSustacaoHook = () => {
  const { setResponse } = useResponse();
  const [pTitulo, setPTitulo] = useState<TituloListItem | null>(null);

  const sustarTitulo = async (id: number, payload: PTituloSustacaoFormInterface) => {
    const response = await PTituloSustacaoService(id, payload);

    if (isTituloListItem(response)) {
      setPTitulo(response);
      setResponse({ status: 200, message: 'Sustação registrada com sucesso' });
    } else {
      setResponse(response);
    }

    return response;
  };

  return { pTitulo, sustarTitulo };
};
