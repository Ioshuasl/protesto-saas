'use server';

import { GSISTEMA_ENDPOINTS } from '@/packages/administrativo/data/GSistema/gsistemaDataConfig';
import type { GSistemaInterface } from '@/packages/administrativo/interfaces/GSistema/GSistemaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGSistemaDeleteData(data: GSistemaInterface) {
  const api = new API();
  return api.send({
    method: Methods.DELETE,
    endpoint: GSISTEMA_ENDPOINTS.delete(data.sistema_id),
  });
}

export const GSistemaDeleteData = withClientErrorHandler(executeGSistemaDeleteData);
