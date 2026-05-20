import { useCallback, useState } from 'react';

import { PTituloProximoNumeroApontamentoService } from '@/packages/administrativo/services/PTitulo/PTituloProximoNumeroApontamentoService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloProximoNumeroApontamentoHook = () => {
  const { setResponse } = useResponse();
  const [proximoNumeroApontamento, setProximoNumeroApontamento] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchProximoNumeroApontamento = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PTituloProximoNumeroApontamentoService();
      if (typeof response === 'number' && !Number.isNaN(response) && response > 0) {
        setProximoNumeroApontamento(response);
      } else {
        setResponse(response);
      }
      return response;
    } finally {
      setIsLoading(false);
    }
  }, [setResponse]);

  return { proximoNumeroApontamento, isLoading, fetchProximoNumeroApontamento };
};
