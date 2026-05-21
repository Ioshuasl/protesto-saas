'use server';

import { PESPECIE_ENDPOINTS } from '@/packages/administrativo/data/PEspecie/pespecieDataConfig';
import type { PEspecieInterface } from '@/packages/administrativo/interfaces/PEspecie/PEspecieInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePEspecieSaveCreateData(
  data: Omit<PEspecieInterface, 'especie_id'>,
): Promise<PEspecieInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: PESPECIE_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PEspecieInterface;
  }

  throw new Error(response?.message ?? 'Erro ao cadastrar espécie');
}

async function executePEspecieSaveUpdateData(
  id: number,
  data: Partial<PEspecieInterface>,
): Promise<PEspecieInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: PESPECIE_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PEspecieInterface;
  }

  throw new Error(response?.message ?? 'Erro ao atualizar espécie');
}

export const PEspecieSaveCreateData = withClientErrorHandler(executePEspecieSaveCreateData);
export const PEspecieSaveUpdateData = withClientErrorHandler(executePEspecieSaveUpdateData);
