'use server';

import GUsuarioIndexData from '@/packages/administrativo/data/GUsuario/GUsuarioIndexData';
import GUsuarioIndexInterface from '@/packages/administrativo/interfaces/GUsuario/GUsuarioIndexInterface';

export default async function GUsuarioIndex(data: GUsuarioIndexInterface) {
  const response = await GUsuarioIndexData(data);

  return response;
}
