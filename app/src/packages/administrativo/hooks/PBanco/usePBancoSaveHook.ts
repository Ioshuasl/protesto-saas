import { useState } from 'react';

import { BancoFormValues } from '@/packages/administrativo/schemas/PBanco/PBancoFormSchema';
import { PBancoInterface } from '@/packages/administrativo/interfaces/PBanco/PBancoInterface';
import { PBancoSaveCreateService } from '@/packages/administrativo/services/PBanco/PBancoSaveCreateService';
import { PBancoSaveUpdateService } from '@/packages/administrativo/services/PBanco/PBancoSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePBancoSaveHook = () => {
  const { setResponse } = useResponse();
  const [pBanco, setPBanco] = useState<PBancoInterface | null>(null);
  // controla se o formulário está aberto ou fechado
  const [isOpen, setIsOpen] = useState(false);

  const saveBanco = async (data: BancoFormValues, selected: PBancoInterface | null) => {
    const response = selected
      ? await PBancoSaveUpdateService(selected.banco_id, data)
      : await PBancoSaveCreateService(data);

    if (response && typeof response === 'object' && 'banco_id' in response) {
      setPBanco(response as PBancoInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'banco_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected ? 'Banco atualizado com sucesso' : 'Banco criado com sucesso',
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

  return { pBanco, saveBanco };
};
