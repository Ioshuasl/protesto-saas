'use server';

import { GFERIADO_ENDPOINTS } from '@/packages/administrativo/data/GFeriado/gferiadoDataConfig';
import type { GFeriadoInterface } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGFeriadoSaveCreateData(
  data: Omit<GFeriadoInterface, 'feriado_id'>,
): Promise<GFeriadoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: GFERIADO_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GFeriadoInterface;
  }

  throw new Error(
    typeof response?.message === 'string' ? response.message : 'Não foi possível salvar o feriado',
  );
}

async function executeGFeriadoSaveUpdateData(
  id: number,
  data: Partial<GFeriadoInterface>,
): Promise<GFeriadoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: GFERIADO_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as GFeriadoInterface;
  }

  throw new Error(
    typeof response?.message === 'string' ? response.message : 'Não foi possível atualizar o feriado',
  );
}

export const GFeriadoSaveCreateData = withClientErrorHandler(executeGFeriadoSaveCreateData);
export const GFeriadoSaveUpdateData = withClientErrorHandler(executeGFeriadoSaveUpdateData);
