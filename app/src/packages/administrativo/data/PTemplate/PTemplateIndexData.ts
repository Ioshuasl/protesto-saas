'use server';

import { PTEMPLATE_ENDPOINTS } from '@/packages/administrativo/data/PTemplate/pTemplateDataConfig';
import type { PTemplateIndexQuery } from '@/packages/administrativo/interfaces/PTemplate/PTemplateIndexQuery';
import type { PTemplateIndexResult } from '@/packages/administrativo/interfaces/PTemplate/PTemplateIndexResult';
import type { PTemplateInterface } from '@/packages/administrativo/interfaces/PTemplate/PTemplateInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from '@/shared/components/pagination';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildPTemplateIndexEndpoint(query?: PTemplateIndexQuery): string {
  const params = new URLSearchParams();

  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set('p', String(page));
  params.set('per_page', String(perPage));
  params.set('sort', query?.sort ?? 'template_id.desc');

  if (query?.descricao) params.set('descricao', query.descricao);
  if (query?.template_id !== undefined) params.set('template_id', String(query.template_id));

  const qs = params.toString();
  return qs ? `${PTEMPLATE_ENDPOINTS.index}?${qs}` : PTEMPLATE_ENDPOINTS.index;
}

function emptyPTemplateIndexResult(
  perPage = DEFAULT_PAGINATION_META.per_page,
): PTemplateIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executePTemplateIndexData(query?: PTemplateIndexQuery): Promise<PTemplateIndexResult> {
  const api = new API();
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPTemplateIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyPTemplateIndexResult(perPage);
  }

  const rows = Array.isArray(response?.data) ? (response.data as PTemplateInterface[]) : [];
  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const PTemplateIndexData = withClientErrorHandler(executePTemplateIndexData);
