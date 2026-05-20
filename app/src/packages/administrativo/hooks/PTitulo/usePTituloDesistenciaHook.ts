import { useState } from 'react';

import type { PTituloDesistenciaFormInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloDesistenciaFormInterface';
import { isTituloListItem, type TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { PTituloDesistenciaService } from '@/packages/administrativo/services/PTitulo/PTituloDesistenciaService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloDesistenciaHook = () => {
  const { setResponse } = useResponse();
  const [pTitulo, setPTitulo] = useState<TituloListItem | null>(null);

  const desistirTitulo = async (id: number, payload?: PTituloDesistenciaFormInterface) => {
    const response = await PTituloDesistenciaService(id, payload);

    if (isTituloListItem(response)) {
      setPTitulo(response);
      setResponse({ status: 200, message: 'Desistência do título registrada com sucesso' });
    } else {
      setResponse(response);
    }

    return response;
  };

  return { pTitulo, desistirTitulo };
};
