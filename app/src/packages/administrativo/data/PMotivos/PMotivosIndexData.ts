'use server';

import { PMOTIVOS_ENDPOINTS } from '@/packages/administrativo/data/PMotivos/pmotivosDataConfig';
import type { PMotivosInterface } from '@/packages/administrativo/interfaces/PMotivos/PMotivosInterface';
import type { PMotivosIndexQuery } from '@/packages/administrativo/interfaces/PMotivos/PMotivosIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

const INDEX_PER_PAGE = 500;

function buildPMotivosIndexEndpoint(query?: PMotivosIndexQuery): string {
  const params = new URLSearchParams();
  params.set('p', String(query?.page ?? 1));
  params.set('per_page', String(query?.per_page ?? INDEX_PER_PAGE));
  params.set('sort', 'motivos_id.desc');
  if (query?.descricao?.trim()) params.set('descricao', query.descricao.trim());
  if (query?.situacao) params.set('situacao', query.situacao);
  return `${PMOTIVOS_ENDPOINTS.index}?${params.toString()}`;
}

async function executePMotivosIndexData(query?: PMotivosIndexQuery): Promise<PMotivosInterface[]> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPMotivosIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return [];
  }

  return Array.isArray(response?.data) ? (response.data as PMotivosInterface[]) : [];
}

export const PMotivosIndexData = withClientErrorHandler(executePMotivosIndexData);
