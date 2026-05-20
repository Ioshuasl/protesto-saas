import { useState } from 'react';

import { LivroNaturezaFormValues } from '@/packages/administrativo/schemas/PLivroNatureza/PLivroNaturezaFormSchema';
import { PLivroNaturezaInterface } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface';
import { PLivroNaturezaSaveCreateService } from '@/packages/administrativo/services/PLivroNatureza/PLivroNaturezaSaveCreateService';
import { PLivroNaturezaSaveUpdateService } from '@/packages/administrativo/services/PLivroNatureza/PLivroNaturezaSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePLivroNaturezaSaveHook = () => {
  const { setResponse } = useResponse();
  const [pLivroNatureza, setPLivroNatureza] = useState<PLivroNaturezaInterface | null>(null);
  // controla se o formulário está aberto ou fechado
  const [isOpen, setIsOpen] = useState(false);

  const saveLivroNatureza = async (
    data: LivroNaturezaFormValues,
    selected: PLivroNaturezaInterface | null,
  ) => {
    const response = selected
      ? await PLivroNaturezaSaveUpdateService(selected.livro_natureza_id, data)
      : await PLivroNaturezaSaveCreateService(data);

    if (response && typeof response === 'object' && 'livro_natureza_id' in response) {
      setPLivroNatureza(response as PLivroNaturezaInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'livro_natureza_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected
              ? 'Natureza de livro atualizada com sucesso'
              : 'Natureza de livro criada com sucesso',
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

  return { pLivroNatureza, saveLivroNatureza };
};
