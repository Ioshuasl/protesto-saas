import { PAndamentoDeleteService } from '@/packages/administrativo/services/PAndamento/PAndamentoDeleteService';
import { PAndamentoIndexByTituloService } from '@/packages/administrativo/services/PAndamento/PAndamentoIndexByTituloService';
import { PAndamentoIndexService } from '@/packages/administrativo/services/PAndamento/PAndamentoIndexService';
import { PAndamentoSaveCreateService } from '@/packages/administrativo/services/PAndamento/PAndamentoSaveCreateService';
import { PAndamentoSaveUpdateService } from '@/packages/administrativo/services/PAndamento/PAndamentoSaveUpdateService';
import { PAndamentoShowService } from '@/packages/administrativo/services/PAndamento/PAndamentoShowService';

export const PAndamentoService = {
  getAll: PAndamentoIndexService,
  getAllByTitulo: PAndamentoIndexByTituloService,
  getById: PAndamentoShowService,
  create: PAndamentoSaveCreateService,
  update: PAndamentoSaveUpdateService,
  delete: PAndamentoDeleteService,
};
