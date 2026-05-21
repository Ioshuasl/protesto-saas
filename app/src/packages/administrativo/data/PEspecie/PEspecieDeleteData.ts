'use server';

import { PESPECIE_ENDPOINTS } from '@/packages/administrativo/data/PEspecie/pespecieDataConfig';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePEspecieDeleteData(id: number) {
  const api = new API();
  return await api.send({
    method: Methods.DELETE,
    endpoint: PESPECIE_ENDPOINTS.delete(id),
  });
}

export const PEspecieDeleteData = withClientErrorHandler(executePEspecieDeleteData);
