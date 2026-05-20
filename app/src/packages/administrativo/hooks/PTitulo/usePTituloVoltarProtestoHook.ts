import { useState } from 'react';

import { isTituloListItem, type TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { PTituloVoltarProtestoService } from '@/packages/administrativo/services/PTitulo/PTituloVoltarProtestoService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloVoltarProtestoHook = () => {
  const { setResponse } = useResponse();
  const [pTitulo, setPTitulo] = useState<TituloListItem | null>(null);

  const voltarParaProtesto = async (id: number) => {
    const response = await PTituloVoltarProtestoService(id);

    if (isTituloListItem(response)) {
      setPTitulo(response);
      setResponse({ status: 200, message: 'Título retornado para protesto com sucesso' });
    } else {
      setResponse(response);
    }

    return response;
  };

  return { pTitulo, voltarParaProtesto };
};
