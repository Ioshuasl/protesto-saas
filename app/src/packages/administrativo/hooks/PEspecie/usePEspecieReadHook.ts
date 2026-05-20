import { useCallback, useState } from 'react';

import { PEspecieInterface } from '@/packages/administrativo/interfaces/PEspecie/PEspecieInterface';
import { PEspecieIndexService } from '@/packages/administrativo/services/PEspecie/PEspecieIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePEspecieReadHook = () => {
  const { setResponse } = useResponse();
  const [especies, setEspecies] = useState<PEspecieInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchEspecies = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PEspecieIndexService();
      if (Array.isArray(response)) {
        setEspecies(response);
        setResponse({
          status: 200,
          message: 'Espécies listadas com sucesso',
        });
      } else {
        setEspecies([]);
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

  return { especies, setEspecies, isLoading, fetchEspecies };
};
