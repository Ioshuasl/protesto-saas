import { gusuarioListRef } from '@/packages/administrativo/data/GUsuario/gusuarioInMemory';
import {
  GUSUARIO_FAKE_ENDPOINTS,
  useGUsuarioMockData,
} from '@/packages/administrativo/data/GUsuario/gusuarioDataConfig';
import type { GUsuarioInterface } from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function GUsuarioShowData(id: number): Promise<GUsuarioInterface | undefined> {
  if (!useGUsuarioMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: GUSUARIO_FAKE_ENDPOINTS.show(id),
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as GUsuarioInterface;
    }
  }

  await mockDbDelay(300);
  return gusuarioListRef.current.find((row) => row.usuario_id === id);
}
