import { PMotivosCancelamentoDeleteService } from '@/packages/administrativo/services/PMotivosCancelamento/PMotivosCancelamentoDeleteService';
import { PMotivosCancelamentoIndexService } from '@/packages/administrativo/services/PMotivosCancelamento/PMotivosCancelamentoIndexService';
import { PMotivosCancelamentoSaveCreateService } from '@/packages/administrativo/services/PMotivosCancelamento/PMotivosCancelamentoSaveCreateService';
import { PMotivosCancelamentoSaveUpdateService } from '@/packages/administrativo/services/PMotivosCancelamento/PMotivosCancelamentoSaveUpdateService';
import { PMotivosCancelamentoShowService } from '@/packages/administrativo/services/PMotivosCancelamento/PMotivosCancelamentoShowService';

export const MotivoCancelamentoService = {
  getAll: PMotivosCancelamentoIndexService,
  getById: PMotivosCancelamentoShowService,
  create: PMotivosCancelamentoSaveCreateService,
  update: PMotivosCancelamentoSaveUpdateService,
  delete: PMotivosCancelamentoDeleteService,
};
