import { GEmolumentoItemIndexService } from '@/packages/administrativo/services/GEmolumentoItem/GEmolumentoItemIndexService';
import { GEmolumentoItemSaveService } from '@/packages/administrativo/services/GEmolumentoItem/GEmolumentoItemSaveService';
import { GEmolumentoItemShowService } from '@/packages/administrativo/services/GEmolumentoItem/GEmolumentoItemShowService';
import { GEmolumentoItemUpdateService } from '@/packages/administrativo/services/GEmolumentoItem/GEmolumentoItemUpdateService';

export const GEmolumentoItemService = {
  getAll: GEmolumentoItemIndexService,
  getById: GEmolumentoItemShowService,
  create: GEmolumentoItemSaveService,
  update: GEmolumentoItemUpdateService,
};
