'use client';

import { useState } from 'react';

import { useResponse } from '@/shared/components/response/ResponseContext';

import { OnlyOfficeEditorTokenService } from '../services/OnlyOfficeEditorTokenService';

export const useTokenOnlyOfficeEditorHook = () => {
  const { setResponse } = useResponse();

  const [onlyOfficeToken, setOnlyOfficeToken] = useState<string>();

  const tokenOnlyOfficeEditorHook = async (data: object) => {
    // Busca as confgiurações do editor
    const response = await OnlyOfficeEditorTokenService(data);

    // Armazena os dados consultados
    setOnlyOfficeToken(response.data);

    // Define a resposta (toast, modal, feedback, etc.)
    setResponse(response);

    // Retorna os dados imediatamente
    return response.data;
  };

  return {
    onlyOfficeToken,
    tokenOnlyOfficeEditorHook,
  };
};
