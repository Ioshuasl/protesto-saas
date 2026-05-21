'use server';

import { PESPECIE_ENDPOINTS } from '@/packages/administrativo/data/PEspecie/pespecieDataConfig';
import type { PEspecieInterface } from '@/packages/administrativo/interfaces/PEspecie/PEspecieInterface';
import type { PEspecieIndexQuery } from '@/packages/administrativo/interfaces/PEspecie/PEspecieIndexQuery';
import type { PEspecieIndexResult } from '@/packages/administrativo/interfaces/PEspecie/PEspecieIndexResult';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from '@/shared/components/pagination';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildPEspecieIndexEndpoint(query?: PEspecieIndexQuery): string {
  const params = new URLSearchParams();

  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set('p', String(page));
  params.set('per_page', String(perPage));
  params.set('sort', query?.sort ?? 'especie_id.desc');

  if (query?.busca) params.set('busca', query.busca);

  const qs = params.toString();
  return qs ? `${PESPECIE_ENDPOINTS.index}?${qs}` : PESPECIE_ENDPOINTS.index;
}

function emptyPEspecieIndexResult(perPage = DEFAULT_PAGINATION_META.per_page): PEspecieIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executePEspecieIndexData(query?: PEspecieIndexQuery): Promise<PEspecieIndexResult> {
  const api = new API();
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPEspecieIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyPEspecieIndexResult(perPage);
  }

  const rows = Array.isArray(response?.data) ? (response.data as PEspecieInterface[]) : [];
  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const PEspecieIndexData = withClientErrorHandler(executePEspecieIndexData);
