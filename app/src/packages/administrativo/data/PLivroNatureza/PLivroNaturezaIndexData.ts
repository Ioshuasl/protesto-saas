'use server';

import { PLIVRO_NATUREZA_ENDPOINTS } from '@/packages/administrativo/data/PLivroNatureza/plivroNaturezaDataConfig';
import type { PLivroNaturezaInterface } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface';
import type { PLivroNaturezaIndexQuery } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaIndexQuery';
import type { PLivroNaturezaIndexResult } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaIndexResult';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from '@/shared/components/pagination';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildPLivroNaturezaIndexEndpoint(query?: PLivroNaturezaIndexQuery): string {
  const params = new URLSearchParams();

  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set('p', String(page));
  params.set('per_page', String(perPage));
  params.set('sort', query?.sort ?? 'livro_natureza_id.desc');

  if (query?.busca) params.set('busca', query.busca);

  const qs = params.toString();
  return qs ? `${PLIVRO_NATUREZA_ENDPOINTS.index}?${qs}` : PLIVRO_NATUREZA_ENDPOINTS.index;
}

function emptyPLivroNaturezaIndexResult(
  perPage = DEFAULT_PAGINATION_META.per_page,
): PLivroNaturezaIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executePLivroNaturezaIndexData(
  query?: PLivroNaturezaIndexQuery,
): Promise<PLivroNaturezaIndexResult> {
  const api = new API();
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPLivroNaturezaIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyPLivroNaturezaIndexResult(perPage);
  }

  const rows = Array.isArray(response?.data)
    ? (response.data as PLivroNaturezaInterface[])
    : [];
  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const PLivroNaturezaIndexData = withClientErrorHandler(executePLivroNaturezaIndexData);
