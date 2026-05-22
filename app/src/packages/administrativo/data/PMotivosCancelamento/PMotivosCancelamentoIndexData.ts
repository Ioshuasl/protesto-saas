'use server';

import { PMOTIVOS_CANCELAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PMotivosCancelamento/pmotivosCancelamentoDataConfig';
import type { PMotivosCancelamentoInterface } from '@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoInterface';
import type { PMotivosCancelamentoIndexQuery } from '@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

const INDEX_PER_PAGE = 500;

function buildPMotivosCancelamentoIndexEndpoint(
  query?: PMotivosCancelamentoIndexQuery,
): string {
  const params = new URLSearchParams();
  params.set('p', String(query?.page ?? 1));
  params.set('per_page', String(query?.per_page ?? INDEX_PER_PAGE));
  params.set('sort', 'motivos_cancelamento_id.desc');
  if (query?.descricao?.trim()) {
    params.set('descricao', query.descricao.trim());
  }
  return `${PMOTIVOS_CANCELAMENTO_ENDPOINTS.index}?${params.toString()}`;
}

async function executePMotivosCancelamentoIndexData(
  query?: PMotivosCancelamentoIndexQuery,
): Promise<PMotivosCancelamentoInterface[]> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPMotivosCancelamentoIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return [];
  }

  return Array.isArray(response?.data)
    ? (response.data as PMotivosCancelamentoInterface[])
    : [];
}

export const PMotivosCancelamentoIndexData = withClientErrorHandler(
  executePMotivosCancelamentoIndexData,
);
