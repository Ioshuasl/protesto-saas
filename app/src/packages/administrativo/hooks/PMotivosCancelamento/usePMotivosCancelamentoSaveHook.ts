import { useState } from 'react';

import type { PMotivosCancelamentoInterface } from '@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoInterface';
import type { MotivoCancelamentoFormValues } from '@/packages/administrativo/schemas/PMotivosCancelamento/PMotivosCancelamentoFormSchema';
import { PMotivosCancelamentoSaveCreateService } from '@/packages/administrativo/services/PMotivosCancelamento/PMotivosCancelamentoSaveCreateService';
import { PMotivosCancelamentoSaveUpdateService } from '@/packages/administrativo/services/PMotivosCancelamento/PMotivosCancelamentoSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePMotivosCancelamentoSaveHook = () => {
  const { setResponse } = useResponse();
  const [pMotivosCancelamento, setPMotivosCancelamento] = useState<PMotivosCancelamentoInterface | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const saveMotivoCancelamento = async (
    data: MotivoCancelamentoFormValues,
    selected: PMotivosCancelamentoInterface | null,
  ) => {
    const response = selected
      ? await PMotivosCancelamentoSaveUpdateService(selected.motivos_cancelamento_id, data)
      : await PMotivosCancelamentoSaveCreateService(data);

    if (response && typeof response === 'object' && 'motivos_cancelamento_id' in response) {
      setPMotivosCancelamento(response as PMotivosCancelamentoInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'motivos_cancelamento_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected
              ? 'Motivo de cancelamento atualizado com sucesso'
              : 'Motivo de cancelamento criado com sucesso',
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

  return { pMotivosCancelamento, saveMotivoCancelamento };
};
