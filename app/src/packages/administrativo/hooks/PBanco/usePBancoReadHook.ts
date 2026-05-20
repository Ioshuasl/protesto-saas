import { useCallback, useState } from 'react';

import { PBancoInterface } from '@/packages/administrativo/interfaces/PBanco/PBancoInterface';
import { PBancoIndexService } from '@/packages/administrativo/services/PBanco/PBancoIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePBancoReadHook = () => {
  const { setResponse } = useResponse();
  const [bancos, setBancos] = useState<PBancoInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchBancos = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PBancoIndexService();
      if (Array.isArray(response)) {
        setBancos(response);
        setResponse({
          status: 200,
          message: 'Bancos listados com sucesso',
        });
      } else {
        setBancos([]);
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

  return { bancos, setBancos, isLoading, fetchBancos };
};
