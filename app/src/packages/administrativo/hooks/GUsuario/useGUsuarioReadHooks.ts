'use client';

import { useState } from 'react';

import Usuario from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import GUsuarioRead from '@/packages/administrativo/services/GUsuario/GUsuarioRead';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGUsuarioReadHooks = () => {
  const { setResponse } = useResponse();

  const [usuario, setUsuario] = useState<Usuario>();

  const fetchUsuario = async (Usuario: Usuario) => {
    const response = await GUsuarioRead(Usuario.usuario_id);
    setUsuario(response.data);
    setResponse(response);
  };

  return { usuario, fetchUsuario };
};
