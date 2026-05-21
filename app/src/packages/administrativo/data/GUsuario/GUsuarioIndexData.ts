'use server';

import GUsuarioIndexInterface from '@/packages/administrativo/interfaces/GUsuario/GUsuarioIndexInterface';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export default async function GUsuarioIndexData(data?: GUsuarioIndexInterface) {
  const api = new API();

  // Monta query string de forma segura, sem adicionar "/" após os parâmetros
  const queryBuilder = data?.urlParams ? `?${new URLSearchParams(data.urlParams).toString()}` : '';

  const response = await api.send({
    method: Methods.GET,
    endpoint: `administrativo/g_usuario/${queryBuilder}`,
  });

  return response;
}
