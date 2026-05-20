import { useCallback, useState } from 'react';

import type { PTituloShowDevedoresItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloShowDevedoresItem';
import { PTituloShowDevedoresService } from '@/packages/administrativo/services/PTitulo/PTituloShowDevedoresService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloShowDevedoresHook = () => {
  const { setResponse } = useResponse();
  const [devedores, setDevedores] = useState<PTituloShowDevedoresItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchDevedores = useCallback(
    async (tituloId: number) => {
      setIsLoading(true);
      try {
        const response = await PTituloShowDevedoresService(tituloId);
        if (Array.isArray(response)) {
          setDevedores(response);
          setResponse({
            status: 200,
            message: 'Devedores do título listados com sucesso',
          });
        } else {
          setDevedores([]);
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
    },
    [setResponse],
  );

  return { devedores, setDevedores, isLoading, fetchDevedores };
};

