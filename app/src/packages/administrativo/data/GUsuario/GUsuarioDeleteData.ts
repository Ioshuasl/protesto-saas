'use server';

import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

type GUsuarioDeletePayload = {
  usuario_id: number;
};

async function executeGUsuarioDeleteData(data: GUsuarioDeletePayload) {

  const api = new API();

  const response = await api.send({
    method: Methods.DELETE,
    endpoint: `administrativo/g_usuario/${data.usuario_id}`,
  });

  return response;
}

export const GUsuarioDeleteData = withClientErrorHandler(executeGUsuarioDeleteData);