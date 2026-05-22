'use server';

import { enrichTituloFromApi } from '@/packages/administrativo/data/PTitulo/ptituloApiMappers';
import { PTITULO_ENDPOINTS } from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import type { PTituloInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloInterface';
import type { TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePTituloShowData(id: number): Promise<TituloListItem | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: PTITULO_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return enrichTituloFromApi(response.data as PTituloInterface);
  }

  return undefined;
}

export const PTituloShowData = withClientErrorHandler(executePTituloShowData);
