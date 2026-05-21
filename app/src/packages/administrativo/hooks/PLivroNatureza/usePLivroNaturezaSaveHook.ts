import { useState } from 'react';

import type { PLivroNaturezaSavePayload } from '@/packages/administrativo/data/PLivroNatureza/PLivroNaturezaSaveData';
import { PLivroNaturezaInterface } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface';
import { LivroNaturezaFormValues } from '@/packages/administrativo/schemas/PLivroNatureza/PLivroNaturezaFormSchema';
import { PLivroNaturezaSaveCreateService } from '@/packages/administrativo/services/PLivroNatureza/PLivroNaturezaSaveCreateService';
import { PLivroNaturezaSaveUpdateService } from '@/packages/administrativo/services/PLivroNatureza/PLivroNaturezaSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

function toSavePayload(data: LivroNaturezaFormValues): PLivroNaturezaSavePayload {
  return {
    sigla: data.sigla,
    descricao: data.descricao,
    situacao: data.situacao,
  };
}

export const usePLivroNaturezaSaveHook = () => {
  const { setResponse } = useResponse();
  const [pLivroNatureza, setPLivroNatureza] = useState<PLivroNaturezaInterface | null>(null);

  const saveLivroNatureza = async (
    data: LivroNaturezaFormValues,
    selected: PLivroNaturezaInterface | null,
  ) => {
    const payload = toSavePayload(data);
    const response = selected
      ? await PLivroNaturezaSaveUpdateService(selected.livro_natureza_id, payload)
      : await PLivroNaturezaSaveCreateService(payload);

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

    return response;
  };

  return { pLivroNatureza, saveLivroNatureza };
};
