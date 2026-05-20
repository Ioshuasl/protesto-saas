import { PLivroNaturezaDeleteService } from '@/packages/administrativo/services/PLivroNatureza/PLivroNaturezaDeleteService';
import { PLivroNaturezaIndexService } from '@/packages/administrativo/services/PLivroNatureza/PLivroNaturezaIndexService';
import { PLivroNaturezaSaveCreateService } from '@/packages/administrativo/services/PLivroNatureza/PLivroNaturezaSaveCreateService';
import { PLivroNaturezaSaveUpdateService } from '@/packages/administrativo/services/PLivroNatureza/PLivroNaturezaSaveUpdateService';
import { PLivroNaturezaShowService } from '@/packages/administrativo/services/PLivroNatureza/PLivroNaturezaShowService';

export const LivroNaturezaService = {
  getAll: PLivroNaturezaIndexService,
  getById: PLivroNaturezaShowService,
  create: PLivroNaturezaSaveCreateService,
  update: PLivroNaturezaSaveUpdateService,
  delete: PLivroNaturezaDeleteService,
};
