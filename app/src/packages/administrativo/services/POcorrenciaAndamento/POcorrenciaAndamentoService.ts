import { POcorrenciaAndamentoDeleteService } from '@/packages/administrativo/services/POcorrenciaAndamento/POcorrenciaAndamentoDeleteService';
import { POcorrenciaAndamentoIndexService } from '@/packages/administrativo/services/POcorrenciaAndamento/POcorrenciaAndamentoIndexService';
import { POcorrenciaAndamentoSaveCreateService } from '@/packages/administrativo/services/POcorrenciaAndamento/POcorrenciaAndamentoSaveCreateService';
import { POcorrenciaAndamentoSaveUpdateService } from '@/packages/administrativo/services/POcorrenciaAndamento/POcorrenciaAndamentoSaveUpdateService';
import { POcorrenciaAndamentoShowService } from '@/packages/administrativo/services/POcorrenciaAndamento/POcorrenciaAndamentoShowService';

export const OcorrenciaAndamentoService = {
  getAll: POcorrenciaAndamentoIndexService,
  getById: POcorrenciaAndamentoShowService,
  create: POcorrenciaAndamentoSaveCreateService,
  update: POcorrenciaAndamentoSaveUpdateService,
  delete: POcorrenciaAndamentoDeleteService,
};
