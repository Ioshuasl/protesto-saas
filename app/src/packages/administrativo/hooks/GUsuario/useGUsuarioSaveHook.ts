'use client';

import { useState } from 'react';

import Usuario from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import GUsuarioSave from '@/packages/administrativo/services/GUsuario/GUsuarioSave';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGUsuarioSaveHook = () => {
  const { setResponse } = useResponse();

  const [GUsuario, setUsuario] = useState<Usuario>();

  const saveGUsuario = async (Usuario: any) => {
    const response = await GUsuarioSave(Usuario);

    setUsuario(response.data);

    setResponse(response);
  };

  return { 
    saveGUsuario, 
    GUsuario };
};
