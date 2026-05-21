'use server';

 import { GUsuarioFormInterface } from '@/packages/administrativo/interfaces/GUsuario/GUsuarioFormInterface';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';
import ApiResponseInterface from '@/shared/services/api/interfaces/ApiResponseInterface';

export default async function GUsuarioSaveData(data: GUsuarioFormInterface): Promise<ApiResponseInterface> {

  // Verifica se existe ID para decidir se é atualização (PUT) ou criação (POST)
  const isUpdate = Boolean(data.usuario_id);

  const api = new API();

  const response = await api.send({
    method: isUpdate ? Methods.PUT : Methods.POST, // PUT se atualizar, POST se criar
    endpoint: `administrativo/g_usuario/${data.usuario_id || ''}`,
    body: data,
  });

  return response;
}
