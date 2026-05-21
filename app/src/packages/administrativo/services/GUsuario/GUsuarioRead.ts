'use server';

import GUsuarioReadData from '@/packages/administrativo/data/GUsuario/GUsuarioReadData';

export default async function GUsuarioRead(usuarioId: number) {
  // Verifica se o id informado é válido
  if (usuarioId <= 0) {
    return {
      code: 400,
      message: 'Usuário informado inválido',
    };
  }

  const response = await GUsuarioReadData(usuarioId);
  return response;
}
