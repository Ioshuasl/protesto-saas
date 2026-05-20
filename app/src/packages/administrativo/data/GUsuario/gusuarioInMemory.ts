import db from '@/db.json';
import type { GUsuarioInterface } from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';

export const gusuarioListRef: { current: GUsuarioInterface[] } = {
  current: [...(db.usuarios || [])],
};
