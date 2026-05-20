import { useCallback, useState } from 'react';

import { GUsuarioInterface } from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import { GUsuarioIndexService } from '@/packages/administrativo/services/GUsuario/GUsuarioIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGUsuarioReadHook = () => {
  const { setResponse } = useResponse();
  const [usuarios, setUsuarios] = useState<GUsuarioInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchUsuarios = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await GUsuarioIndexService();
      if (Array.isArray(response)) {
        setUsuarios(response);
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
