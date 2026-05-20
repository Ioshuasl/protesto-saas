import { useCallback, useState } from 'react';

import type { PMotivosCancelamentoInterface } from '@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoInterface';
import { PMotivosCancelamentoIndexService } from '@/packages/administrativo/services/PMotivosCancelamento/PMotivosCancelamentoIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePMotivosCancelamentoReadHook = () => {
  const { setResponse } = useResponse();
  const [motivosCancelamento, setMotivosCancelamento] = useState<PMotivosCancelamentoInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchMotivosCancelamento = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PMotivosCancelamentoIndexService();
      if (Array.isArray(response)) {
        setMotivosCancelamento(response);
        setResponse({
          status: 200,
          message: 'Motivos de cancelamento listados com sucesso',
        });
      } else {
        setMotivosCancelamento([]);
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

  return { motivosCancelamento, setMotivosCancelamento, isLoading, fetchMotivosCancelamento };
};
