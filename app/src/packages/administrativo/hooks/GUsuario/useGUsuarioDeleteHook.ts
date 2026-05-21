import { useState } from 'react';


import GUsuarioInterface from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import { GUsuarioDeleteService } from '@/packages/administrativo/services/GUsuario/GUsuarioDeleteService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGUsuarioDeleteHook = () => {
  const { setResponse } = useResponse();

  const [GUsuario, setGUsuario] = useState<GUsuarioInterface>();

  const deleteGUsuario = async (data: GUsuarioInterface) => {
    const response = await GUsuarioDeleteService(data);

    setGUsuario(data);
    setResponse(response);
  };

  return { GUsuario, deleteGUsuario };
};
