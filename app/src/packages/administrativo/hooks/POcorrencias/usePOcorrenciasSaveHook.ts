import { useState } from 'react';

import type { POcorrenciasInterface } from '@/packages/administrativo/interfaces/POcorrencias/POcorrenciasInterface';
import type { OcorrenciaFormValues } from '@/packages/administrativo/schemas/POcorrencias/POcorrenciasFormSchema';
import { POcorrenciasSaveCreateService } from '@/packages/administrativo/services/POcorrencias/POcorrenciasSaveCreateService';
import { POcorrenciasSaveUpdateService } from '@/packages/administrativo/services/POcorrencias/POcorrenciasSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePOcorrenciasSaveHook = () => {
  const { setResponse } = useResponse();
  const [pOcorrencias, setPOcorrencias] = useState<POcorrenciasInterface | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const saveOcorrencia = async (data: OcorrenciaFormValues, selected: POcorrenciasInterface | null) => {
    const response = selected
      ? await POcorrenciasSaveUpdateService(selected.ocorrencias_id, data)
      : await POcorrenciasSaveCreateService(data);

    if (response && typeof response === 'object' && 'ocorrencias_id' in response) {
      setPOcorrencias(response as POcorrenciasInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'ocorrencias_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected
              ? 'Ocorrência atualizada com sucesso'
              : 'Ocorrência criada com sucesso',
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

  return { pOcorrencias, saveOcorrencia };
};
