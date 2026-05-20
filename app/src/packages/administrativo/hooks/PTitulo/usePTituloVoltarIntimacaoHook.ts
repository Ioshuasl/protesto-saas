import { useState } from 'react';

import { isTituloListItem, type TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import type { PTituloVoltarIntimacaoInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloVoltarIntimacaoInterface';
import { PTituloVoltarIntimacaoService } from '@/packages/administrativo/services/PTitulo/PTituloVoltarIntimacaoService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloVoltarIntimacaoHook = () => {
  const { setResponse } = useResponse();
  const [pTitulo, setPTitulo] = useState<TituloListItem | null>(null);

  const voltarParaIntimacao = async (id: number, payload: PTituloVoltarIntimacaoInterface) => {
    const response = await PTituloVoltarIntimacaoService(id, payload);

    if (isTituloListItem(response)) {
      setPTitulo(response);
      setResponse({ status: 200, message: 'Título retornado para intimação com sucesso' });
    } else {
      setResponse(response);
    }

    return response;
  };

  return { pTitulo, voltarParaIntimacao };
};
