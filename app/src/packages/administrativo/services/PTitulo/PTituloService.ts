import { PTituloIndexService } from '@/packages/administrativo/services/PTitulo/PTituloIndexService';
import { PTituloSaveUpdateStatusService } from '@/packages/administrativo/services/PTitulo/PTituloSaveUpdateStatusService';
import { PTituloShowService } from '@/packages/administrativo/services/PTitulo/PTituloShowService';

export const TituloService = {
  getAll: PTituloIndexService,
  getById: PTituloShowService,
  updateStatus: PTituloSaveUpdateStatusService,
};

export type { TituloListItem, TituloStatus } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
