import { GUsuarioDeleteService } from '@/packages/administrativo/services/GUsuario/GUsuarioDeleteService';
import { GUsuarioIndexService } from '@/packages/administrativo/services/GUsuario/GUsuarioIndexService';
import { GUsuarioSaveCreateService } from '@/packages/administrativo/services/GUsuario/GUsuarioSaveCreateService';
import { GUsuarioSaveUpdateService } from '@/packages/administrativo/services/GUsuario/GUsuarioSaveUpdateService';
import { GUsuarioShowService } from '@/packages/administrativo/services/GUsuario/GUsuarioShowService';

export const UsuarioService = {
  getAll: GUsuarioIndexService,
  getById: GUsuarioShowService,
  create: GUsuarioSaveCreateService,
  update: GUsuarioSaveUpdateService,
  delete: GUsuarioDeleteService,
};
