'use server';

import GUsuarioSaveData from '@/packages/administrativo/data/GUsuario/GUsuarioSaveData';

export default async function GUsuarioSave(form: any) {
  return await GUsuarioSaveData(form);
}
