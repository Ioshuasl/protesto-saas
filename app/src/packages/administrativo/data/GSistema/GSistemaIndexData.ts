'use server';

import { GSISTEMA_ENDPOINTS } from '@/packages/administrativo/data/GSistema/gsistemaDataConfig';
import type { GSistemaInterface } from '@/packages/administrativo/interfaces/GSistema/GSistemaInterface';
import type { GSistemaIndexQuery } from '@/packages/administrativo/interfaces/GSistema/GSistemaIndexQuery';
import type { GSistemaIndexResult } from '@/packages/administrativo/interfaces/GSistema/GSistemaIndexResult';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from '@/shared/components/pagination';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildGSistemaIndexEndpoint(query?: GSistemaIndexQuery): string {
  const params = new URLSearchParams();

  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set('p', String(page));
  params.set('per_page', String(perPage));

  if (query?.sort) params.set('sort', query.sort);
  if (query?.descricao) params.set('descricao', query.descricao);
  if (query?.situacao) params.set('situacao', query.situacao);
  if (query?.tipo_cartorio) params.set('tipo_cartorio', query.tipo_cartorio);

  const qs = params.toString();
  return qs ? `${GSISTEMA_ENDPOINTS.index}?${qs}` : GSISTEMA_ENDPOINTS.index;
}

function emptyGSistemaIndexResult(perPage = DEFAULT_PAGINATION_META.per_page): GSistemaIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executeGSistemaIndexData(query?: GSistemaIndexQuery): Promise<GSistemaIndexResult> {
  const api = new API();
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  const response = await api.send({
    method: Methods.GET,
    endpoint: buildGSistemaIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyGSistemaIndexResult(perPage);
  }

  const rows = Array.isArray(response?.data) ? (response.data as GSistemaInterface[]) : [];
  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const GSistemaIndexData = withClientErrorHandler(executeGSistemaIndexData);
