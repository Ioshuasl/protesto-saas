import { useCallback, useState } from 'react';

import { PLivroNaturezaInterface } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface';
import { PLivroNaturezaIndexService } from '@/packages/administrativo/services/PLivroNatureza/PLivroNaturezaIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePLivroNaturezaReadHook = () => {
  const { setResponse } = useResponse();
  const [naturezas, setNaturezas] = useState<PLivroNaturezaInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchNaturezas = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PLivroNaturezaIndexService();
      if (Array.isArray(response)) {
        setNaturezas(response);
        setResponse({
          status: 200,
          message: 'Naturezas de livro listadas com sucesso',
        });
      } else {
        setNaturezas([]);
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

  return { naturezas, setNaturezas, isLoading, fetchNaturezas };
};
