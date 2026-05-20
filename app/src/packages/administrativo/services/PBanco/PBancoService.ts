import { PBancoDeleteService } from '@/packages/administrativo/services/PBanco/PBancoDeleteService';
import { PBancoIndexService } from '@/packages/administrativo/services/PBanco/PBancoIndexService';
import { PBancoSaveCreateService } from '@/packages/administrativo/services/PBanco/PBancoSaveCreateService';
import { PBancoSaveUpdateService } from '@/packages/administrativo/services/PBanco/PBancoSaveUpdateService';
import { PBancoShowService } from '@/packages/administrativo/services/PBanco/PBancoShowService';

export const BancoService = {
  getAll: PBancoIndexService,
  getById: PBancoShowService,
  create: PBancoSaveCreateService,
  update: PBancoSaveUpdateService,
  delete: PBancoDeleteService,
};
