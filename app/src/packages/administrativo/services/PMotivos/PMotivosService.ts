import { PMotivosDeleteService } from '@/packages/administrativo/services/PMotivos/PMotivosDeleteService';
import { PMotivosIndexService } from '@/packages/administrativo/services/PMotivos/PMotivosIndexService';
import { PMotivosSaveCreateService } from '@/packages/administrativo/services/PMotivos/PMotivosSaveCreateService';
import { PMotivosSaveUpdateService } from '@/packages/administrativo/services/PMotivos/PMotivosSaveUpdateService';
import { PMotivosShowService } from '@/packages/administrativo/services/PMotivos/PMotivosShowService';

export const MotivoService = {
  getAll: PMotivosIndexService,
  getById: PMotivosShowService,
  create: PMotivosSaveCreateService,
  update: PMotivosSaveUpdateService,
  delete: PMotivosDeleteService,
};
