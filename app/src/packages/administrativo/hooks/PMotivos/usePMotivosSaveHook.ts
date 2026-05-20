import { useState } from 'react';

import { MotivoFormValues } from '@/packages/administrativo/schemas/PMotivos/PMotivosFormSchema';
import { PMotivosInterface } from '@/packages/administrativo/interfaces/PMotivos/PMotivosInterface';
import { PMotivosSaveCreateService } from '@/packages/administrativo/services/PMotivos/PMotivosSaveCreateService';
import { PMotivosSaveUpdateService } from '@/packages/administrativo/services/PMotivos/PMotivosSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePMotivosSaveHook = () => {
  const { setResponse } = useResponse();
  const [pMotivos, setPMotivos] = useState<PMotivosInterface | null>(null);
  // controla se o formulário está aberto ou fechado
  const [isOpen, setIsOpen] = useState(false);

  const saveMotivo = async (data: MotivoFormValues, selected: PMotivosInterface | null) => {
    const response = selected
      ? await PMotivosSaveUpdateService(selected.motivos_id, data)
      : await PMotivosSaveCreateService(data);

    if (response && typeof response === 'object' && 'motivos_id' in response) {
      setPMotivos(response as PMotivosInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'motivos_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected ? 'Motivo atualizado com sucesso' : 'Motivo criado com sucesso',
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

  return { pMotivos, saveMotivo };
};
