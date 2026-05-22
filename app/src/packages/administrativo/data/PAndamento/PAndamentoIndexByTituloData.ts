'use server';

import { PANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PAndamento/pAndamentoDataConfig';
import type { PAndamentoInterface } from '@/packages/administrativo/interfaces/PAndamento/PAndamentoInterface';
import type { PAndamentoIndexQuery } from '@/packages/administrativo/interfaces/PAndamento/PAndamentoIndexQuery';
import type { PAndamentoIndexResult } from '@/packages/administrativo/interfaces/PAndamento/PAndamentoIndexResult';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from '@/shared/components/pagination';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildPAndamentoIndexByTituloEndpoint(
  tituloId: number,
  query?: Omit<PAndamentoIndexQuery, 'titulo_id'>,
): string {
  const params = new URLSearchParams();

  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set('p', String(page));
  params.set('per_page', String(perPage));
  params.set('sort', query?.sort ?? 'andamento_id.desc');

  if (query?.ocorrencia_andamento_id != null) {
    params.set('ocorrencia_andamento_id', String(query.ocorrencia_andamento_id));
  }
  if (query?.data_ocorrencia?.trim()) {
    params.set('data_ocorrencia', query.data_ocorrencia.trim());
  }

  const qs = params.toString();
  const base = PANDAMENTO_ENDPOINTS.indexByTitulo(tituloId);
  return qs ? `${base}?${qs}` : base;
}

function emptyPAndamentoIndexResult(
  perPage = DEFAULT_PAGINATION_META.per_page,
): PAndamentoIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executePAndamentoIndexByTituloData(
  tituloId: number,
  query?: Omit<PAndamentoIndexQuery, 'titulo_id'>,
): Promise<PAndamentoIndexResult> {
  const api = new API();
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPAndamentoIndexByTituloEndpoint(tituloId, query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyPAndamentoIndexResult(perPage);
  }

  const rows = Array.isArray(response?.data)
    ? (response.data as PAndamentoInterface[])
    : [];
  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const PAndamentoIndexByTituloData = withClientErrorHandler(
  executePAndamentoIndexByTituloData,
);
