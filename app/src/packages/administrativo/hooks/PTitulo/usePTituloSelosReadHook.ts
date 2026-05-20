import { useCallback, useState } from 'react';

import type { PTituloSeloVinculadoItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloSeloVinculadoItem';
import { PTituloSelosIndexService } from '@/packages/administrativo/services/PTitulo/PTituloSelosIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloSelosReadHook = () => {
  const { setResponse } = useResponse();
  const [selos, setSelos] = useState<PTituloSeloVinculadoItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchSelos = useCallback(
    async (id: number) => {
      setIsLoading(true);
      try {
        const response = await PTituloSelosIndexService(id);
        if (Array.isArray(response)) {
          setSelos(response);
          setResponse({
            status: 200,
            message: 'Selos listados com sucesso',
          });
        } else {
          setSelos([]);
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

  return { selos, setSelos, isLoading, fetchSelos };
};
