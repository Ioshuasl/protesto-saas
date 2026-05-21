'use server';

import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export type GUsuarioAuth2FARequestPayload = {
  identificador: string;
  senha_api: string;
  codigo_seguranca: string;
};

export default async function GUsuarioAuth2FAData(payload: GUsuarioAuth2FARequestPayload) {
  const api = new API();

  const response = (await api.send({
    method: Methods.POST,
    endpoint: `administrativo/g_usuario/authenticate`,
    body: {
      identificador: payload.identificador.trim(),
      senha_api: payload.senha_api,
      codigo_seguranca: payload.codigo_seguranca,
    },
  })) as Record<string, unknown>;

  return response;
}
