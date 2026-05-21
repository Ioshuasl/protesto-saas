'use server';

import GUsuarioMeData from '@/packages/administrativo/data/GUsuario/GUsuarioMeData';

export default async function GUsuarioMeService() {
  return await GUsuarioMeData();
}
