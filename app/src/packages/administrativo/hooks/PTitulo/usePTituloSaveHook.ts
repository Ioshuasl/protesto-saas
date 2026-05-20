import { useState } from 'react';

import {
  isTituloListItem,
  type TituloListItem,
  type TituloStatus,
} from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { PTituloSaveUpdateStatusService } from '@/packages/administrativo/services/PTitulo/PTituloSaveUpdateStatusService';
import { useResponse } from '@/shared/components/response/ResponseContext';

/** No protótipo, “save” de título no grid é atualização de status (sem create/delete mock). */
export const usePTituloSaveHook = () => {
  const { setResponse } = useResponse();
  const [pTitulo, setPTitulo] = useState<TituloListItem | null>(null);

  const saveTituloStatus = async (tituloId: number, status: TituloStatus) => {
    const response = await PTituloSaveUpdateStatusService(tituloId, status);

    if (isTituloListItem(response)) {
      setPTitulo(response);
    }

    setResponse(
      isTituloListItem(response)
        ? {
            status: 200,
            message: 'Status do título atualizado com sucesso',
          }
        : {
            status: (response as { status?: number }).status,
            message: (response as { message?: string }).message,
            error: (response as { message?: string }).message,
          },
    );

    return response;
  };

  return { pTitulo, saveTituloStatus };
};
