import { PEspecieDeleteService } from '@/packages/administrativo/services/PEspecie/PEspecieDeleteService';
import { PEspecieIndexService } from '@/packages/administrativo/services/PEspecie/PEspecieIndexService';
import { PEspecieSaveCreateService } from '@/packages/administrativo/services/PEspecie/PEspecieSaveCreateService';
import { PEspecieSaveUpdateService } from '@/packages/administrativo/services/PEspecie/PEspecieSaveUpdateService';
import { PEspecieShowService } from '@/packages/administrativo/services/PEspecie/PEspecieShowService';

export const EspecieService = {
  getAll: PEspecieIndexService,
  getById: PEspecieShowService,
  create: PEspecieSaveCreateService,
  update: PEspecieSaveUpdateService,
  delete: PEspecieDeleteService,
};
