'use server';

import { G_EMOLUMENTO_ITEM_ENDPOINTS } from '@/packages/administrativo/data/GEmolumentoItem/gEmolumentoItemDataConfig';
import type {
  GEmolumentoListInterface,
  GEmolumentoListQuery,
  GEmolumentoListResult,
} from '@/packages/administrativo/interfaces/GEmolumentoList/GEmolumentoListInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from '@/shared/components/pagination';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildGEmolumentoListEndpoint(query?: GEmolumentoListQuery): string {
  const params = new URLSearchParams();

  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set('p', String(page));
  params.set('per_page', String(perPage));
  params.set('sort', query?.sort ?? 'selo_grupo_id.asc');

  if (query?.emolumento_periodo_id !== undefined) {
    params.set('emolumento_periodo_id', String(query.emolumento_periodo_id));
  }

  if (query?.sistema_id != null) {
    params.set('sistema_id', String(query.sistema_id));
  }

  const busca = query?.busca?.trim();
  if (busca) {
    params.set('busca', busca);
  }

  const qs = params.toString();
  return qs
    ? `${G_EMOLUMENTO_ITEM_ENDPOINTS.listDetails}?${qs}`
    : G_EMOLUMENTO_ITEM_ENDPOINTS.listDetails;
}

function emptyGEmolumentoListResult(perPage = DEFAULT_PAGINATION_META.per_page): GEmolumentoListResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executeGEmolumentoListData(
  query?: GEmolumentoListQuery,
): Promise<GEmolumentoListResult> {
  const api = new API();
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;
  const response = await api.send({
    method: Methods.GET,
    endpoint: buildGEmolumentoListEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyGEmolumentoListResult(perPage);
  }

  const rows = Array.isArray(response?.data) ? (response.data as GEmolumentoListInterface[]) : [];
  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const GEmolumentoListData = withClientErrorHandler(executeGEmolumentoListData);
