import { useState } from 'react';

import { EspecieFormValues } from '@/packages/administrativo/schemas/PEspecie/PEspecieFormSchema';
import { PEspecieInterface } from '@/packages/administrativo/interfaces/PEspecie/PEspecieInterface';
import { PEspecieSaveCreateService } from '@/packages/administrativo/services/PEspecie/PEspecieSaveCreateService';
import { PEspecieSaveUpdateService } from '@/packages/administrativo/services/PEspecie/PEspecieSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePEspecieSaveHook = () => {
  const { setResponse } = useResponse();
  const [pEspecie, setPEspecie] = useState<PEspecieInterface | null>(null);
  // controla se o formulário está aberto ou fechado
  const [isOpen, setIsOpen] = useState(false);

  const saveEspecie = async (data: EspecieFormValues, selected: PEspecieInterface | null) => {
    const response = selected
      ? await PEspecieSaveUpdateService(selected.especie_id, data)
      : await PEspecieSaveCreateService(data);

    if (response && typeof response === 'object' && 'especie_id' in response) {
      setPEspecie(response as PEspecieInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'especie_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected ? 'Espécie atualizada com sucesso' : 'Espécie criada com sucesso',
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

  return { pEspecie, saveEspecie };
};
