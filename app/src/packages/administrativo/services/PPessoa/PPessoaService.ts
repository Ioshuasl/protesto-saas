import { PPessoaDeleteService } from '@/packages/administrativo/services/PPessoa/PPessoaDeleteService';
import { PPessoaIndexService } from '@/packages/administrativo/services/PPessoa/PPessoaIndexService';
import type { PPessoaIndexQuery } from '@/packages/administrativo/interfaces/PPessoa/PPessoaIndexQuery';
import type { PPessoaIndexResult } from '@/packages/administrativo/interfaces/PPessoa/PPessoaIndexResult';
import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';
import { PPessoaSaveCreateService } from '@/packages/administrativo/services/PPessoa/PPessoaSaveCreateService';
import { PPessoaSaveUpdateService } from '@/packages/administrativo/services/PPessoa/PPessoaSaveUpdateService';
import { PPessoaShowService } from '@/packages/administrativo/services/PPessoa/PPessoaShowService';

function isPPessoaIndexResult(value: unknown): value is PPessoaIndexResult {
  return (
    typeof value === 'object' &&
    value !== null &&
    Array.isArray((value as PPessoaIndexResult).rows) &&
    typeof (value as PPessoaIndexResult).pagination === 'object'
  );
}

/** Fachada compatível com telas legadas — operações mapeiam para *Index/Show/Save/Delete*Service. */
export const PessoaService = {
  getAll: async (query?: PPessoaIndexQuery): Promise<PPessoaInterface[]> => {
    const response = await PPessoaIndexService(query);
    if (isPPessoaIndexResult(response)) {
      return response.rows;
    }
    return [];
  },
  getById: PPessoaShowService,
  create: PPessoaSaveCreateService,
  update: PPessoaSaveUpdateService,
  delete: PPessoaDeleteService,
};
