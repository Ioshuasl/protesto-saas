import { useCallback, useState } from 'react';

import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';
import { PPessoaIndexService } from '@/packages/administrativo/services/PPessoa/PPessoaIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

/** Equivalente ao `useTCensecReadHook`: carrega a lista via serviço de index. */
export const usePPessoaReadHook = () => {
  const { setResponse } = useResponse();
  const [pessoas, setPessoas] = useState<PPessoaInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchPessoas = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PPessoaIndexService();
      if (Array.isArray(response)) {
        setPessoas(response);
        setResponse({
          status: 200,
          message: 'Pessoas listadas com sucesso',
        });
      } else {
        setPessoas([]);
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

  return { pessoas, setPessoas, isLoading, fetchPessoas };
};
