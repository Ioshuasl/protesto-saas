import { useState } from 'react';

import { GUsuarioDeleteData } from '@/packages/administrativo/data/GUsuario/GUsuarioDeleteData';
import { GUsuarioInterface } from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGUsuarioDeleteHook = () => {
  const { setResponse } = useResponse();

  const [gUsuario, setGUsuario] = useState<GUsuarioInterface>();

  const deleteGUsuario = async (data: GUsuarioInterface) => {
    const response = await GUsuarioDeleteData(data);

    setGUsuario(data);

    setResponse(response);
  };

  return { gUsuario, deleteGUsuario };
};
