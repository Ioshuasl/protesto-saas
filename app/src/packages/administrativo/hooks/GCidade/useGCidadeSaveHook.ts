import { useState } from 'react';

import GCidadeInterface from '@/packages/administrativo/interfaces/GCidade/GCidadeInterface';
import { GCidadeSaveService } from '@/packages/administrativo/services/GCidade/GCidadeSaveService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGCidadeSaveHook = () => {
  const { setResponse } = useResponse();
  const [gCidade, setGCidade] = useState<GCidadeInterface | null>(null);

  const saveGCidade = async (data: GCidadeInterface) => {
    const response = await GCidadeSaveService(data);

    // Guardar os dados localizados
    setGCidade(response.data);

    // Manda a resposta para o verificador de resposta
    setResponse(response);
  };

  return { gCidade, saveGCidade };
};
