import { PLivroAndamentoDeleteService } from '@/packages/administrativo/services/PLivroAndamento/PLivroAndamentoDeleteService';
import { PLivroAndamentoIndexService } from '@/packages/administrativo/services/PLivroAndamento/PLivroAndamentoIndexService';
import { PLivroAndamentoSaveCreateService } from '@/packages/administrativo/services/PLivroAndamento/PLivroAndamentoSaveCreateService';
import { PLivroAndamentoSaveUpdateService } from '@/packages/administrativo/services/PLivroAndamento/PLivroAndamentoSaveUpdateService';
import { PLivroAndamentoShowService } from '@/packages/administrativo/services/PLivroAndamento/PLivroAndamentoShowService';

export const LivroAndamentoService = {
  getAll: PLivroAndamentoIndexService,
  getById: PLivroAndamentoShowService,
  create: PLivroAndamentoSaveCreateService,
  update: PLivroAndamentoSaveUpdateService,
  delete: PLivroAndamentoDeleteService,
};
