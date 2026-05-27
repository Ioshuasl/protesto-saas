'use server';

import { G_EMOLUMENTO_PERIODO_ENDPOINTS } from '@/packages/administrativo/data/GEmolumentoPeriodo/gEmolumentoPeriodoDataConfig';
import type { GEmolumentoPeriodoInterface } from '@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGEmolumentoPeriodoDeleteData(data: GEmolumentoPeriodoInterface) {
  const api = new API();
  return api.send({
    method: Methods.DELETE,
    endpoint: G_EMOLUMENTO_PERIODO_ENDPOINTS.delete(data.emolumento_periodo_id),
  });
}

export const GEmolumentoPeriodoDeleteData = withClientErrorHandler(
  executeGEmolumentoPeriodoDeleteData,
);
