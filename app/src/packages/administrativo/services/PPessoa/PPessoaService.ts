import { PPessoaDeleteService } from '@/packages/administrativo/services/PPessoa/PPessoaDeleteService';
import { PPessoaIndexService } from '@/packages/administrativo/services/PPessoa/PPessoaIndexService';
import { PPessoaSaveCreateService } from '@/packages/administrativo/services/PPessoa/PPessoaSaveCreateService';
import { PPessoaSaveUpdateService } from '@/packages/administrativo/services/PPessoa/PPessoaSaveUpdateService';
import { PPessoaShowService } from '@/packages/administrativo/services/PPessoa/PPessoaShowService';

/** Fachada compatível com telas legadas — operações mapeiam para *Index/Show/Save/Delete*Service. */
export const PessoaService = {
  getAll: PPessoaIndexService,
  getById: PPessoaShowService,
  create: PPessoaSaveCreateService,
  update: PPessoaSaveUpdateService,
  delete: PPessoaDeleteService,
};
