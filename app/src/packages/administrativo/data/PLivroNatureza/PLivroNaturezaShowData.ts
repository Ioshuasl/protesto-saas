'use server';

import { PLIVRO_NATUREZA_ENDPOINTS } from '@/packages/administrativo/data/PLivroNatureza/plivroNaturezaDataConfig';
import type { PLivroNaturezaInterface } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePLivroNaturezaShowData(
  id: number,
): Promise<PLivroNaturezaInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: PLIVRO_NATUREZA_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PLivroNaturezaInterface;
  }

  return undefined;
}

export const PLivroNaturezaShowData = withClientErrorHandler(executePLivroNaturezaShowData);
