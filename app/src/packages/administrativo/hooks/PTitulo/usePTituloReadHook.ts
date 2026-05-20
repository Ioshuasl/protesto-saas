import { useCallback, useState } from 'react';

import type { TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { PTituloIndexService } from '@/packages/administrativo/services/PTitulo/PTituloIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloReadHook = () => {
  const { setResponse } = useResponse();
  const [titulos, setTitulos] = useState<TituloListItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchTitulos = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PTituloIndexService();
      if (Array.isArray(response)) {
        setTitulos(response);
        setResponse({
          status: 200,
          message: 'Títulos listados com sucesso',
        });
      } else {
        setTitulos([]);
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

  return { titulos, setTitulos, isLoading, fetchTitulos };
};
