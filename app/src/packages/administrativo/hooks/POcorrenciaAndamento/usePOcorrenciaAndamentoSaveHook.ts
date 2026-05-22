import { useState } from 'react';

import type { POcorrenciaAndamentoInterface } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface';
import type { OcorrenciaAndamentoFormValues } from '@/packages/administrativo/schemas/POcorrenciaAndamento/POcorrenciaAndamentoFormSchema';
import { POcorrenciaAndamentoSaveCreateService } from '@/packages/administrativo/services/POcorrenciaAndamento/POcorrenciaAndamentoSaveCreateService';
import { POcorrenciaAndamentoSaveUpdateService } from '@/packages/administrativo/services/POcorrenciaAndamento/POcorrenciaAndamentoSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePOcorrenciaAndamentoSaveHook = () => {
  const { setResponse } = useResponse();
  const [pOcorrenciaAndamento, setPOcorrenciaAndamento] =
    useState<POcorrenciaAndamentoInterface | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const saveOcorrenciaAndamento = async (
    data: OcorrenciaAndamentoFormValues,
    selected: POcorrenciaAndamentoInterface | null,
  ) => {
    const response = selected
      ? await POcorrenciaAndamentoSaveUpdateService(
          selected.ocorrencia_andamento_id,
          data,
        )
      : await POcorrenciaAndamentoSaveCreateService(data);

    if (
      response &&
      typeof response === 'object' &&
      'ocorrencia_andamento_id' in response
    ) {
      setPOcorrenciaAndamento(response as POcorrenciaAndamentoInterface);
    }

    setResponse(
      response &&
        typeof response === 'object' &&
        'ocorrencia_andamento_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected
              ? 'Ocorrência de andamento atualizada com sucesso'
              : 'Ocorrência de andamento criada com sucesso',
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

  return { pOcorrenciaAndamento, saveOcorrenciaAndamento, isOpen, setIsOpen };
};
