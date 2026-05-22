'use client';

import { useState } from 'react';

import GUfInterface from '@/packages/administrativo/interfaces/GUF/GUfInterface';
import GUfIndexService from '@/packages/administrativo/services/GUF/GUfIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGUfReadHook = () => {
  const { setResponse } = useResponse();

  // Controle dos dados obtidos via API
  const [gUf, setGUf] = useState<GUfInterface[]>([]);

  const fetchGUf = async () => {
    // Realiza a requisição para a api
    const response = await GUfIndexService();

    // Armazena os dados da resposta
    setGUf(response.data);

    // Envia os dados da resposta para ser tratado
    setResponse(response);
  };

  return { gUf, fetchGUf };
};
