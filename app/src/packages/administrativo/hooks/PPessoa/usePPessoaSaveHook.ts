import { useState } from 'react';

import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';
import type { PessoaFormValues } from '@/packages/administrativo/schemas/PPessoa/PPessoaFormSchema';
import { PPessoaSaveCreateService } from '@/packages/administrativo/services/PPessoa/PPessoaSaveCreateService';
import { PPessoaSaveUpdateService } from '@/packages/administrativo/services/PPessoa/PPessoaSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePPessoaSaveHook = () => {
  const { setResponse } = useResponse();
  const [pPessoa, setPPessoa] = useState<PPessoaInterface | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const savePessoa = async (data: PessoaFormValues, selected: PPessoaInterface | null) => {
    const payload = {
      ...data,
      data_nascimento: data.data_nascimento || undefined,
    };

    const response = selected
      ? await PPessoaSaveUpdateService(selected.pessoa_id, payload)
      : await PPessoaSaveCreateService(payload as Omit<PPessoaInterface, 'pessoa_id'>);

    if (response && typeof response === 'object' && 'pessoa_id' in response) {
      setPPessoa(response as PPessoaInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'pessoa_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected ? 'Pessoa atualizada com sucesso' : 'Pessoa criada com sucesso',
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

  return { pPessoa, savePessoa };
};
