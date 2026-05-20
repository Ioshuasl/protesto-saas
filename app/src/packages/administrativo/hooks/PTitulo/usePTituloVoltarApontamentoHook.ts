import { useState } from 'react';

import { isTituloListItem, type TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import type { PTituloVoltarApontamentoInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloVoltarApontamentoInterface';
import { PTituloVoltarApontamentoService } from '@/packages/administrativo/services/PTitulo/PTituloVoltarApontamentoService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloVoltarApontamentoHook = () => {
  const { setResponse } = useResponse();
  const [pTitulo, setPTitulo] = useState<TituloListItem | null>(null);

  const voltarParaApontamento = async (id: number, payload: PTituloVoltarApontamentoInterface) => {
    const response = await PTituloVoltarApontamentoService(id, payload);

    if (isTituloListItem(response)) {
      setPTitulo(response);
      setResponse({ status: 200, message: 'Título retornado para apontamento com sucesso' });
    } else {
      setResponse(response);
    }

    return response;
  };

  return { pTitulo, voltarParaApontamento };
};
