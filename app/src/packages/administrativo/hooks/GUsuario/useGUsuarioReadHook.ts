import { useCallback, useState } from 'react';

import GUsuarioInterface from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import { GUsuarioIndexService } from '@/packages/administrativo/services/GUsuario/GUsuarioIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

function resolveUsuariosResponse(response: unknown): GUsuarioInterface[] | null {
  if (Array.isArray(response)) {
    return response as GUsuarioInterface[];
  }

  if (response && typeof response === 'object' && Array.isArray((response as { data?: unknown }).data)) {
    return (response as { data: GUsuarioInterface[] }).data;
  }

  return null;
}

export const useGUsuarioReadHook = () => {
  const { setResponse } = useResponse();
  const [usuarios, setUsuarios] = useState<GUsuarioInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchUsuarios = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await GUsuarioIndexService();
      const rows = resolveUsuariosResponse(response);

      if (rows) {
        setUsuarios(rows);
        setResponse({
          status: 200,
          message: 'Usuários listados com sucesso',
        });
      } else {
        setUsuarios([]);
        setResponse({
          status: response.status,
          message: response.message,
          error: response.message,
        });
      }
      return response;
    } finally {
      setIsLoading(false);
    }
  }, [setResponse]);

  return { usuarios, setUsuarios, isLoading, fetchUsuarios };
};
