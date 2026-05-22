'use server';

import { POCORRENCIA_ANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/POcorrenciaAndamento/pocorrenciaAndamentoDataConfig';
import type { POcorrenciaAndamentoInterface } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface';
import type { POcorrenciaAndamentoIndexQuery } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoIndexQuery';
import type { POcorrenciaAndamentoIndexResult } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoIndexResult';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from '@/shared/components/pagination';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildPOcorrenciaAndamentoIndexEndpoint(
  query?: POcorrenciaAndamentoIndexQuery,
): string {
  const params = new URLSearchParams();

  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set('p', String(page));
  params.set('per_page', String(perPage));
  params.set('sort', query?.sort ?? 'ocorrencia_andamento_id.desc');

  if (query?.descricao?.trim()) params.set('descricao', query.descricao.trim());

  const qs = params.toString();
  return qs ? `${POCORRENCIA_ANDAMENTO_ENDPOINTS.index}?${qs}` : POCORRENCIA_ANDAMENTO_ENDPOINTS.index;
}

function emptyPOcorrenciaAndamentoIndexResult(
  perPage = DEFAULT_PAGINATION_META.per_page,
): POcorrenciaAndamentoIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executePOcorrenciaAndamentoIndexData(
  query?: POcorrenciaAndamentoIndexQuery,
): Promise<POcorrenciaAndamentoIndexResult> {
  const api = new API();
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPOcorrenciaAndamentoIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyPOcorrenciaAndamentoIndexResult(perPage);
  }

  const rows = Array.isArray(response?.data)
    ? (response.data as POcorrenciaAndamentoInterface[])
    : [];
  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const POcorrenciaAndamentoIndexData = withClientErrorHandler(
  executePOcorrenciaAndamentoIndexData,
);
