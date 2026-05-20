'use client';

import { useState } from 'react';

import GGramaticaInterface from '@/packages/administrativo/interfaces/GGramatica/GGramaticaInterface';
import { useResponse } from '@/shared/components/response/ResponseContext';
import useGUsuarioGetJWTHook from '@/shared/hooks/auth/useGUsuarioGetJWTHook';

import { OnlyOfficeEditorPrepareService } from '../services/OnlyOfficeEditorPrepareService';

export const usePrepareOnlyOfficeEditorHook = () => {
  const { setResponse } = useResponse();
  const { fetchToken } = useGUsuarioGetJWTHook();

  const [onlyOfficeEditor, setOnlyOfficeEditor] = useState<GGramaticaInterface[]>([]);

  const prepareOnlyOfficeEditorHook = async () => {
    // Busca as confgiurações do editor
    const response = await OnlyOfficeEditorPrepareService();

    // Obtem o usuário logado
    const user = await fetchToken();

    // Busca os dados do usuário
    response.data.user = user?.data;

    // Armazena os dados consultados
    setOnlyOfficeEditor(response.data);

    // Define a resposta (toast, modal, feedback, etc.)
    setResponse(response);

    // Retorna os dados imediatamente
    return response;
  };

  return {
    onlyOfficeEditor,
    prepareOnlyOfficeEditorHook,
  };
};
