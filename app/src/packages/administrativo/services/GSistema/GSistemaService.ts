import { GSistemaDeleteService } from '@/packages/administrativo/services/GSistema/GSistemaDeleteService';
import { GSistemaIndexService } from '@/packages/administrativo/services/GSistema/GSistemaIndexService';
import { GSistemaSaveCreateService } from '@/packages/administrativo/services/GSistema/GSistemaSaveCreateService';
import { GSistemaSaveUpdateService } from '@/packages/administrativo/services/GSistema/GSistemaSaveUpdateService';
import { GSistemaShowService } from '@/packages/administrativo/services/GSistema/GSistemaShowService';

export const SistemaService = {
  getAll: GSistemaIndexService,
  getById: GSistemaShowService,
  create: GSistemaSaveCreateService,
  update: GSistemaSaveUpdateService,
  delete: GSistemaDeleteService,
};
