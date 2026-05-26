import { GEmolumentoDeleteService } from '@/packages/administrativo/services/GEmolumento/GEmolumentoDeleteService';
import { GEmolumentoIndexService } from '@/packages/administrativo/services/GEmolumento/GEmolumentoIndexService';
import { GEmolumentoSaveCreateService } from '@/packages/administrativo/services/GEmolumento/GEmolumentoSaveCreateService';
import { GEmolumentoSaveUpdateService } from '@/packages/administrativo/services/GEmolumento/GEmolumentoSaveUpdateService';
import { GEmolumentoShowService } from '@/packages/administrativo/services/GEmolumento/GEmolumentoShowService';

export const EmolumentoService = {
  getAll: GEmolumentoIndexService,
  getById: GEmolumentoShowService,
  create: GEmolumentoSaveCreateService,
  update: GEmolumentoSaveUpdateService,
  delete: GEmolumentoDeleteService,
};
