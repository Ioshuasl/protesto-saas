import { POcorrenciasDeleteService } from '@/packages/administrativo/services/POcorrencias/POcorrenciasDeleteService';
import { POcorrenciasIndexService } from '@/packages/administrativo/services/POcorrencias/POcorrenciasIndexService';
import { POcorrenciasSaveCreateService } from '@/packages/administrativo/services/POcorrencias/POcorrenciasSaveCreateService';
import { POcorrenciasSaveUpdateService } from '@/packages/administrativo/services/POcorrencias/POcorrenciasSaveUpdateService';
import { POcorrenciasShowService } from '@/packages/administrativo/services/POcorrencias/POcorrenciasShowService';

export const OcorrenciaService = {
  getAll: POcorrenciasIndexService,
  getById: POcorrenciasShowService,
  create: POcorrenciasSaveCreateService,
  update: POcorrenciasSaveUpdateService,
  delete: POcorrenciasDeleteService,
};
