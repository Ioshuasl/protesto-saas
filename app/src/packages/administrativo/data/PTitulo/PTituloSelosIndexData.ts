import { PTITULO_ENDPOINTS } from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import { sortPTituloSelosVinculados } from '@/packages/administrativo/data/PTitulo/ptituloSelosUtils';
import type { PTituloSeloVinculadoItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloSeloVinculadoItem';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePTituloSelosIndexData(id: number): Promise<PTituloSeloVinculadoItem[]> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: PTITULO_ENDPOINTS.selos(id),
  });

  if (
    Number(response?.status) >= 200 &&
    Number(response?.status) < 300 &&
    Array.isArray(response?.data)
  ) {
    return sortPTituloSelosVinculados(response.data as PTituloSeloVinculadoItem[]);
  }

  return [];
}

export const PTituloSelosIndexData = withClientErrorHandler(executePTituloSelosIndexData);
