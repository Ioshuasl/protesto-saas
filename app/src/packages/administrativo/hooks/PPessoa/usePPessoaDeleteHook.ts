import { useState } from 'react';

import { PPessoaDeleteData } from '@/packages/administrativo/data/PPessoa/PPessoaDeleteData';
import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePPessoaDeleteHook = () => {
  const { setResponse } = useResponse();

  const [pPessoa, setPPessoa] = useState<PPessoaInterface>();

  const deletePessoa = async (pessoaId: number) => {
    const response = await PPessoaDeleteData(pessoaId);

    setPPessoa({ pessoa_id: pessoaId } as PPessoaInterface);

    setResponse(response);
    return response;
  };

  return { pPessoa, deletePessoa };
};
