import { useState } from 'react';

import type { GSistemaInterface } from '@/packages/administrativo/interfaces/GSistema/GSistemaInterface';
import { GSistemaSaveCreateService } from '@/packages/administrativo/services/GSistema/GSistemaSaveCreateService';
import { GSistemaSaveUpdateService } from '@/packages/administrativo/services/GSistema/GSistemaSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGSistemaSaveHook = () => {
  const { setResponse } = useResponse();
  const [gSistema, setGSistema] = useState<GSistemaInterface | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const saveSistema = async (
    data: GSistemaInterface | Partial<Omit<GSistemaInterface, 'sistema_id'>>,
    selected: GSistemaInterface | null,
  ) => {
    const response = selected
      ? await GSistemaSaveUpdateService(
          selected.sistema_id,
          data as Partial<Omit<GSistemaInterface, 'sistema_id'>>,
        )
      : await GSistemaSaveCreateService(data as GSistemaInterface);

    if (response && typeof response === 'object' && 'sistema_id' in response) {
      setGSistema(response as GSistemaInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'sistema_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected ? 'Sistema atualizado com sucesso' : 'Sistema criado com sucesso',
          }
        : {
            status: (response as { status?: number }).status,
            message: (response as { message?: string }).message,
            error: (response as { message?: string }).message,
          },
    );

    setIsOpen(false);

    return response;
  };

  return { gSistema, saveSistema, isOpen, setIsOpen };
};
