import { useState } from 'react';

import type { PTituloIntimacaoInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloIntimacaoInterface';
import { isTituloListItem, type TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { PTituloIntimacaoService } from '@/packages/administrativo/services/PTitulo/PTituloIntimacaoService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloIntimacaoHook = () => {
  const { setResponse } = useResponse();
  const [pTitulo, setPTitulo] = useState<TituloListItem | null>(null);

  const intimarTitulo = async (id: number, payload: PTituloIntimacaoInterface) => {
    const response = await PTituloIntimacaoService(id, payload);

    if (isTituloListItem(response)) {
      setPTitulo(response);
      setResponse({ status: 200, message: 'Título intimado com sucesso' });
    } else {
      setResponse(response);
    }

    return response;
  };

  return { pTitulo, intimarTitulo };
};
