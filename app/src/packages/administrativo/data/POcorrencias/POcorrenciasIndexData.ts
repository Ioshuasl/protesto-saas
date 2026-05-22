'use server';

import { POCORRENCIAS_ENDPOINTS } from '@/packages/administrativo/data/POcorrencias/pocorrenciasDataConfig';
import type { POcorrenciasInterface } from '@/packages/administrativo/interfaces/POcorrencias/POcorrenciasInterface';
import type { POcorrenciasIndexQuery } from '@/packages/administrativo/interfaces/POcorrencias/POcorrenciasIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

const INDEX_PER_PAGE = 500;

function buildPOcorrenciasIndexEndpoint(query?: POcorrenciasIndexQuery): string {
  const params = new URLSearchParams();
  params.set('p', String(query?.page ?? 1));
  params.set('per_page', String(query?.per_page ?? INDEX_PER_PAGE));
  params.set('sort', 'ocorrencias_id.desc');
  if (query?.busca?.trim()) params.set('busca', query.busca.trim());
  if (query?.tipo) params.set('tipo', query.tipo);
  return `${POCORRENCIAS_ENDPOINTS.index}?${params.toString()}`;
}

async function executePOcorrenciasIndexData(
  query?: POcorrenciasIndexQuery,
): Promise<POcorrenciasInterface[]> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPOcorrenciasIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return [];
  }

  return Array.isArray(response?.data) ? (response.data as POcorrenciasInterface[]) : [];
}

export const POcorrenciasIndexData = withClientErrorHandler(executePOcorrenciasIndexData);
