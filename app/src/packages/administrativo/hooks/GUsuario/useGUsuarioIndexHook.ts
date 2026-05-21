'use client';

import { useCallback, useState } from 'react';

import GUsuarioIndexInterface from '@/packages/administrativo/interfaces/GUsuario/GUsuarioIndexInterface';
import GUsuarioInterface from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import GUsuarioIndex from '@/packages/administrativo/services/GUsuario/GUsuarioIndex';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGUsuarioIndexHook = () => {
  const { setResponse } = useResponse();

  const [GUsuario, setUsuarios] = useState<GUsuarioInterface[] | null>(null);

  /**
   * Busca a lista de usuários
   * useCallback evita recriação da função a cada render
   */
  const indexGUsuario = useCallback(async (data: GUsuarioIndexInterface) => {
    const response = await GUsuarioIndex(data);

    // Atualiza estado com os dados retornados
    setUsuarios(response.data);

    // Define os dados do componente de resposta (toast, modal, etc)
    setResponse(response);
  }, [setResponse]);

  return { GUsuario, indexGUsuario };
};