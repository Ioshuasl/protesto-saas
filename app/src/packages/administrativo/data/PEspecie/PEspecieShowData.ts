'use server';

import { PESPECIE_ENDPOINTS } from '@/packages/administrativo/data/PEspecie/pespecieDataConfig';
import type { PEspecieInterface } from '@/packages/administrativo/interfaces/PEspecie/PEspecieInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePEspecieShowData(id: number): Promise<PEspecieInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: PESPECIE_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PEspecieInterface;
  }

  return undefined;
}

export const PEspecieShowData = withClientErrorHandler(executePEspecieShowData);
