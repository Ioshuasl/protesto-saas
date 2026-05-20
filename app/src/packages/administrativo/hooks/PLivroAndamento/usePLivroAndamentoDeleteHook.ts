import { useState } from 'react';

import { PLivroAndamentoDeleteData } from '@/packages/administrativo/data/PLivroAndamento/PLivroAndamentoDeleteData';
import { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePLivroAndamentoDeleteHook = () => {
  const { setResponse } = useResponse();

  const [pLivroAndamento, setPLivroAndamento] = useState<PLivroAndamentoInterface>();

  const deleteLivroAndamento = async (id: number) => {
    const response = await PLivroAndamentoDeleteData(id);

    setPLivroAndamento({ livro_andamento_id: id } as PLivroAndamentoInterface);

    setResponse(response);
    return response;
  };

  return { pLivroAndamento, deleteLivroAndamento };
};
