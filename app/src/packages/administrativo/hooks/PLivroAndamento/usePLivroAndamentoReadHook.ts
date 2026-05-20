import { useCallback, useState } from 'react';

import { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import { PLivroAndamentoIndexService } from '@/packages/administrativo/services/PLivroAndamento/PLivroAndamentoIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePLivroAndamentoReadHook = () => {
  const { setResponse } = useResponse();
  const [livrosAndamento, setLivrosAndamento] = useState<PLivroAndamentoInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchLivrosAndamento = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PLivroAndamentoIndexService();
      if (Array.isArray(response)) {
        setLivrosAndamento(response);
        setResponse({
          status: 200,
          message: 'Livros em andamento listados com sucesso',
        });
      } else {
        setLivrosAndamento([]);
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

  return { livrosAndamento, setLivrosAndamento, isLoading, fetchLivrosAndamento };
};
