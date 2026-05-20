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

async function executeGUsuarioDeleteData(data: GUsuarioInterface) {
  const id = data.usuario_id;
  if (!useGUsuarioMockData()) {
    const api = new API();
    return await api.send({
      method: Methods.DELETE,
      endpoint: GUSUARIO_FAKE_ENDPOINTS.delete(id),
    });
  }

  await mockDbDelay(500);
  gusuarioListRef.current = gusuarioListRef.current.filter((row) => row.usuario_id !== id);

  return {
    status: 200,
    message: 'Usuário removido com sucesso',
    data,
  };
}

export const GUsuarioDeleteData = withClientErrorHandler(executeGUsuarioDeleteData);
