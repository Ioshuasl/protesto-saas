'use client';

import GUsuarioLogoutService from '@/packages/administrativo/services/GUsuario/GUsuarioLogoutService';

export const useGUsuarioLogoutHook = () => {
  const logoutUsuario = async () => {
    await GUsuarioLogoutService('access_token');
  };

  return { logoutUsuario };
};
