'use server';

import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export default async function GUsuarioMeData() {
  const api = new API();

  const response = await api.send({
    method: Methods.GET,
    endpoint: `administrativo/g_usuario/me`,
  });

  return response;
}
