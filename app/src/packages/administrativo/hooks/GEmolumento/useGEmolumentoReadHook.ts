import { useCallback, useState } from 'react';

import type { GEmolumentoIndexQuery } from '@/packages/administrativo/interfaces/GEmolumento/GEmolumentoIndexQuery';
import type { GEmolumentoInterface } from '@/packages/administrativo/interfaces/GEmolumento/GEmolumentoInterface';
import { GEmolumentoIndexService } from '@/packages/administrativo/services/GEmolumento/GEmolumentoIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGEmolumentoReadHook = () => {
  const { setResponse } = useResponse();
  const [emolumentos, setEmolumentos] = useState<GEmolumentoInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchEmolumentos = useCallback(
    async (sistemaId: number, query?: GEmolumentoIndexQuery) => {
      setIsLoading(true);
      try {
        const response = await GEmolumentoIndexService(sistemaId, query);
        if (Array.isArray(response)) {
          setEmolumentos(response);
          setResponse({
            status: 200,
            message: 'Emolumentos listados com sucesso',
          });
        } else {
          setEmolumentos([]);
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

  return { emolumentos, setEmolumentos, isLoading, fetchEmolumentos };
};
