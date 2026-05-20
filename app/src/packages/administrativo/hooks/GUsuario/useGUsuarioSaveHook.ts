import { useState } from 'react';

import { GUsuarioInterface } from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import { GUsuarioSaveCreateService } from '@/packages/administrativo/services/GUsuario/GUsuarioSaveCreateService';
import { GUsuarioSaveUpdateService } from '@/packages/administrativo/services/GUsuario/GUsuarioSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGUsuarioSaveHook = () => {
  const { setResponse } = useResponse();
  const [gUsuario, setGUsuario] = useState<GUsuarioInterface | null>(null);
  // controla se o formulário está aberto ou fechado
  const [isOpen, setIsOpen] = useState(false);

  const saveGUsuario = async (
    data: Omit<GUsuarioInterface, 'usuario_id'> | Partial<GUsuarioInterface>,
    selected: GUsuarioInterface | null,
  ) => {
    const response = selected
      ? await GUsuarioSaveUpdateService(selected.usuario_id, data as Partial<GUsuarioInterface>)
      : await GUsuarioSaveCreateService(data as Omit<GUsuarioInterface, 'usuario_id'>);

    if (response && typeof response === 'object' && 'usuario_id' in response) {
      setGUsuario(response as GUsuarioInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'usuario_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected ? 'Usuário atualizado com sucesso' : 'Usuário criado com sucesso',
          }
        : {
            status: (response as { status?: number }).status,
            message: (response as { message?: string }).message,
            error: (response as { message?: string }).message,
          },
    );

    // Fecha o formulário automaticamente após salvar
    setIsOpen(false);

    // Retorna os dados imediatamente
    return response;
  };

  return { gUsuario, saveGUsuario };
};
