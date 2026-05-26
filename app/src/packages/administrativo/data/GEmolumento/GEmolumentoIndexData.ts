'use server';

import { GEMOLUMENTO_ENDPOINTS } from '@/packages/administrativo/data/GEmolumento/gemolumentoDataConfig';
import type { GEmolumentoIndexQuery } from '@/packages/administrativo/interfaces/GEmolumento/GEmolumentoIndexQuery';
import type { GEmolumentoInterface } from '@/packages/administrativo/interfaces/GEmolumento/GEmolumentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildGEmolumentoIndexEndpoint(sistemaId: number, query?: GEmolumentoIndexQuery): string {
  const params = new URLSearchParams();

  if (query?.situacao) params.set('situacao', query.situacao);

  const qs = params.toString();
  const endpoint = GEMOLUMENTO_ENDPOINTS.indexBySistema(sistemaId);

  return qs ? `${endpoint}?${qs}` : endpoint;
}

async function executeGEmolumentoIndexData(
  sistemaId: number,
  query?: GEmolumentoIndexQuery,
): Promise<GEmolumentoInterface[]> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: buildGEmolumentoIndexEndpoint(sistemaId, query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return [];
  }

  return Array.isArray(response?.data) ? (response.data as GEmolumentoInterface[]) : [];
}

export const GEmolumentoIndexData = withClientErrorHandler(executeGEmolumentoIndexData);
