import { GEmolumentoPeriodoDeleteService } from '@/packages/administrativo/services/GEmolumentoPeriodo/GEmolumentoPeriodoDeleteService';
import { GEmolumentoPeriodoIndexService } from '@/packages/administrativo/services/GEmolumentoPeriodo/GEmolumentoPeriodoIndexService';
import { GEmolumentoPeriodoSaveCreateService } from '@/packages/administrativo/services/GEmolumentoPeriodo/GEmolumentoPeriodoSaveCreateService';
import { GEmolumentoPeriodoSaveUpdateService } from '@/packages/administrativo/services/GEmolumentoPeriodo/GEmolumentoPeriodoSaveUpdateService';
import { GEmolumentoPeriodoShowService } from '@/packages/administrativo/services/GEmolumentoPeriodo/GEmolumentoPeriodoShowService';

export const GEmolumentoPeriodoService = {
  getAll: GEmolumentoPeriodoIndexService,
  getById: GEmolumentoPeriodoShowService,
  create: GEmolumentoPeriodoSaveCreateService,
  update: GEmolumentoPeriodoSaveUpdateService,
  delete: GEmolumentoPeriodoDeleteService,
};
