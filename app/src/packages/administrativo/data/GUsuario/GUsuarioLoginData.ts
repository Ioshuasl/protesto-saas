'use server';

import { GUsuarioLoginFormValues } from '@/packages/administrativo/schemas/GUsuario/GUsuarioLoginSchema';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export default async function GUsuarioLoginData(form: GUsuarioLoginFormValues) {
  const api = new API();

  const response = await api.send({
    method: Methods.POST,
    endpoint: `administrativo/g_usuario/authenticate`,
    body: {
      identificador: form.identificador.trim(),
      senha_api: form.senha_api,
    },
  });

  return response;
}
