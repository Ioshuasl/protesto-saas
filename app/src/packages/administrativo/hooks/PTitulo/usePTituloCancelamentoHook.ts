import { useState } from 'react';

import type { PTituloCancelamentoFormInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloCancelamentoFormInterface';
import { isTituloListItem, type TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { PTituloCancelamentoService } from '@/packages/administrativo/services/PTitulo/PTituloCancelamentoService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloCancelamentoHook = () => {
  const { setResponse } = useResponse();
  const [pTitulo, setPTitulo] = useState<TituloListItem | null>(null);

  const cancelarTitulo = async (id: number, payload?: PTituloCancelamentoFormInterface) => {
    const response = await PTituloCancelamentoService(id, payload);

    if (isTituloListItem(response)) {
      setPTitulo(response);
      setResponse({ status: 200, message: 'Título cancelado com sucesso' });
    } else {
      setResponse(response);
    }

    return response;
  };

  return { pTitulo, cancelarTitulo };
};
