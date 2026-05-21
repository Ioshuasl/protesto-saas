'use server';

import { GFERIADO_ENDPOINTS } from '@/packages/administrativo/data/GFeriado/gferiadoDataConfig';
import type { GFeriadoInterface } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGFeriadoDeleteData(data: GFeriadoInterface) {
  const api = new API();
  return api.send({
    method: Methods.DELETE,
    endpoint: GFERIADO_ENDPOINTS.delete(data.feriado_id),
  });
}

export const GFeriadoDeleteData = withClientErrorHandler(executeGFeriadoDeleteData);
