import { ptituloListRef } from '@/packages/administrativo/data/PTitulo/ptituloInMemory';
import {
  PTITULO_FAKE_ENDPOINTS,
  isPTituloMockDataEnabled,
} from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import type { PTituloSeloVinculadoItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloSeloVinculadoItem';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

interface TituloComSelos {
  vinculos_selos?: PTituloSeloVinculadoItem[];
}

export async function PTituloSelosIndexData(id: number): Promise<PTituloSeloVinculadoItem[]> {
  if (!isPTituloMockDataEnabled()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PTITULO_FAKE_ENDPOINTS.selos(id),
      }),
    );
    const response = await apiCall();
    if (
      Number(response?.status) >= 200 &&
      Number(response?.status) < 300 &&
      Array.isArray(response?.data)
    ) {
      return response.data as PTituloSeloVinculadoItem[];
    }
  }

  await mockDbDelay(200);
  const titulo = ptituloListRef.current.find((row) => row.titulo_id === id) as TituloComSelos | undefined;
  if (!Array.isArray(titulo?.vinculos_selos)) return [];
  return titulo.vinculos_selos.map((selo) => ({ ...selo }));
}
