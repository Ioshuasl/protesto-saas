'use server';

import { PBANCO_ENDPOINTS } from '@/packages/administrativo/data/PBanco/pbancoDataConfig';
import type { PBancoInterface } from '@/packages/administrativo/interfaces/PBanco/PBancoInterface';
import type { PBancoIndexQuery } from '@/packages/administrativo/interfaces/PBanco/PBancoIndexQuery';
import type { PBancoIndexResult } from '@/packages/administrativo/interfaces/PBanco/PBancoIndexResult';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from '@/shared/components/pagination';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildPBancoIndexEndpoint(query?: PBancoIndexQuery): string {
  const params = new URLSearchParams();

  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set('p', String(page));
  params.set('per_page', String(perPage));
  params.set('sort', query?.sort ?? 'banco_id.desc');

  if (query?.busca) params.set('busca', query.busca);

  const qs = params.toString();
  return qs ? `${PBANCO_ENDPOINTS.index}?${qs}` : PBANCO_ENDPOINTS.index;
}

function emptyPBancoIndexResult(perPage = DEFAULT_PAGINATION_META.per_page): PBancoIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executePBancoIndexData(query?: PBancoIndexQuery): Promise<PBancoIndexResult> {
  const api = new API();
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPBancoIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyPBancoIndexResult(perPage);
  }

  const rows = Array.isArray(response?.data) ? (response.data as PBancoInterface[]) : [];
  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const PBancoIndexData = withClientErrorHandler(executePBancoIndexData);
