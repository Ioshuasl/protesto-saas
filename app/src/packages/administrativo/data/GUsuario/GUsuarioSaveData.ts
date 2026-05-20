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

export async function GUsuarioSaveCreateData(
  data: Omit<GUsuarioInterface, 'usuario_id'>,
): Promise<GUsuarioInterface> {
  if (!useGUsuarioMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.POST,
        endpoint: GUSUARIO_FAKE_ENDPOINTS.create,
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as GUsuarioInterface;
    }
  }

  await mockDbDelay(600);
  const list = gusuarioListRef.current;
  const newId = list.length > 0 ? Math.max(...list.map((row) => row.usuario_id)) + 1 : 1;
  const created = { ...data, usuario_id: newId } as GUsuarioInterface;
  list.push(created);
  return created;
}

export async function GUsuarioSaveUpdateData(
  id: number,
  data: Partial<GUsuarioInterface>,
): Promise<GUsuarioInterface> {
  if (!useGUsuarioMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: GUSUARIO_FAKE_ENDPOINTS.update(id),
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as GUsuarioInterface;
    }
  }

  await mockDbDelay(600);
  const list = gusuarioListRef.current;
  const index = list.findIndex((row) => row.usuario_id === id);
  if (index === -1) throw new Error('Usuário não encontrado');
  list[index] = { ...list[index], ...data };
  return list[index];
}
