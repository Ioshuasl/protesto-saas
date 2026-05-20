import { useState } from 'react';

import { PLivroNaturezaDeleteData } from '@/packages/administrativo/data/PLivroNatureza/PLivroNaturezaDeleteData';
import { PLivroNaturezaInterface } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePLivroNaturezaDeleteHook = () => {
  const { setResponse } = useResponse();

  const [pLivroNatureza, setPLivroNatureza] = useState<PLivroNaturezaInterface>();

  const deleteLivroNatureza = async (id: number) => {
    const response = await PLivroNaturezaDeleteData(id);

    setPLivroNatureza({ livro_natureza_id: id } as PLivroNaturezaInterface);

    setResponse(response);
    return response;
  };

  return { pLivroNatureza, deleteLivroNatureza };
};
