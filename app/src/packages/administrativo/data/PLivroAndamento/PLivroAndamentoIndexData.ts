'use server';

import { PLIVRO_ANDAMENTO_ENDPOINTS } from '@/packages/administrativo/data/PLivroAndamento/plivroAndamentoDataConfig';
import type { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import type { PLivroAndamentoIndexQuery } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoIndexQuery';
import type { PLivroAndamentoIndexResult } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoIndexResult';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from '@/shared/components/pagination';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildPLivroAndamentoIndexEndpoint(query?: PLivroAndamentoIndexQuery): string {
  const params = new URLSearchParams();

  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set('p', String(page));
  params.set('per_page', String(perPage));
  params.set('sort', query?.sort ?? 'data_abertura.desc');

  if (query?.busca) params.set('busca', query.busca);
  if (query?.livro_natureza_id != null) {
    params.set('livro_natureza_id', String(query.livro_natureza_id));
  }
  if (query?.aberto) params.set('aberto', query.aberto);

  const qs = params.toString();
  return qs ? `${PLIVRO_ANDAMENTO_ENDPOINTS.index}?${qs}` : PLIVRO_ANDAMENTO_ENDPOINTS.index;
}

function emptyPLivroAndamentoIndexResult(
  perPage = DEFAULT_PAGINATION_META.per_page,
): PLivroAndamentoIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executePLivroAndamentoIndexData(
  query?: PLivroAndamentoIndexQuery,
): Promise<PLivroAndamentoIndexResult> {
  const api = new API();
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPLivroAndamentoIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyPLivroAndamentoIndexResult(perPage);
  }

  const rows = Array.isArray(response?.data)
    ? (response.data as PLivroAndamentoInterface[])
    : [];
  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const PLivroAndamentoIndexData = withClientErrorHandler(executePLivroAndamentoIndexData);
