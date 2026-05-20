import { useState } from 'react';

import { LivroAndamentoFormValues } from '@/packages/administrativo/schemas/PLivroAndamento/PLivroAndamentoFormSchema';
import { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import { PLivroAndamentoSaveCreateService } from '@/packages/administrativo/services/PLivroAndamento/PLivroAndamentoSaveCreateService';
import { PLivroAndamentoSaveUpdateService } from '@/packages/administrativo/services/PLivroAndamento/PLivroAndamentoSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePLivroAndamentoSaveHook = () => {
  const { setResponse } = useResponse();
  const [pLivroAndamento, setPLivroAndamento] = useState<PLivroAndamentoInterface | null>(null);
  // controla se o formulário está aberto ou fechado
  const [isOpen, setIsOpen] = useState(false);

  const saveLivroAndamento = async (
    data: LivroAndamentoFormValues,
    selected: PLivroAndamentoInterface | null,
  ) => {
    const payload = {
      ...data,
      data_abertura: data.data_abertura,
      data_fechamento: data.data_fechamento || undefined,
    };

    const response = selected
      ? await PLivroAndamentoSaveUpdateService(selected.livro_andamento_id, payload)
      : await PLivroAndamentoSaveCreateService(payload);

    if (response && typeof response === 'object' && 'livro_andamento_id' in response) {
      setPLivroAndamento(response as PLivroAndamentoInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'livro_andamento_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected
              ? 'Livro em andamento atualizado com sucesso'
              : 'Livro em andamento criado com sucesso',
          }
        : {
            status: (response as { status?: number }).status,
            message: (response as { message?: string }).message,
            error: (response as { message?: string }).message,
          },
    );

    setIsOpen(false);

    return response;
  };

  return { pLivroAndamento, saveLivroAndamento };
};
