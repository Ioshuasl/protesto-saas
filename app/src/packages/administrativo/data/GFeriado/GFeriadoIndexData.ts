'use server';

import { GFERIADO_ENDPOINTS } from '@/packages/administrativo/data/GFeriado/gferiadoDataConfig';
import type { GFeriadoInterface } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface';
import type { GFeriadoIndexQuery } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoIndexQuery';
import type { GFeriadoIndexResult } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoIndexResult';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from '@/shared/components/pagination';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildGFeriadoIndexEndpoint(query?: GFeriadoIndexQuery): string {
  const params = new URLSearchParams();

  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set('p', String(page));
  params.set('per_page', String(perPage));

  if (query?.tipo) params.set('tipo', query.tipo);
  if (query?.situacao) params.set('situacao', query.situacao);
  if (query?.descricao) params.set('descricao', query.descricao);
  if (query?.ano != null) params.set('ano', String(query.ano));

  const qs = params.toString();
  return qs ? `${GFERIADO_ENDPOINTS.index}?${qs}` : GFERIADO_ENDPOINTS.index;
}

function emptyGFeriadoIndexResult(perPage = DEFAULT_PAGINATION_META.per_page): GFeriadoIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executeGFeriadoIndexData(query?: GFeriadoIndexQuery): Promise<GFeriadoIndexResult> {
  const api = new API();
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  const response = await api.send({
    method: Methods.GET,
    endpoint: buildGFeriadoIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyGFeriadoIndexResult(perPage);
  }

  const rows = Array.isArray(response?.data) ? (response.data as GFeriadoInterface[]) : [];
  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const GFeriadoIndexData = withClientErrorHandler(executeGFeriadoIndexData);
