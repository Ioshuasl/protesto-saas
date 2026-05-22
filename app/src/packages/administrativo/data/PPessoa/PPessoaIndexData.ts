'use server';

import { PPESSOA_ENDPOINTS } from '@/packages/administrativo/data/PPessoa/ppessoaDataConfig';
import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';
import type { PPessoaIndexQuery } from '@/packages/administrativo/interfaces/PPessoa/PPessoaIndexQuery';
import type { PPessoaIndexResult } from '@/packages/administrativo/interfaces/PPessoa/PPessoaIndexResult';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from '@/shared/components/pagination';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildPPessoaIndexEndpoint(query?: PPessoaIndexQuery): string {
  const params = new URLSearchParams();

  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set('p', String(page));
  params.set('per_page', String(perPage));
  params.set('sort', query?.sort ?? 'pessoa_id.desc');

  if (query?.busca?.trim()) params.set('busca', query.busca.trim());
  if (query?.cidade?.trim()) params.set('cidade', query.cidade.trim());
  if (query?.uf?.trim()) params.set('uf', query.uf.trim());
  if (query?.tipo_pessoa === 'F' || query?.tipo_pessoa === 'J') {
    params.set('tipo_pessoa', query.tipo_pessoa);
  }

  return `${PPESSOA_ENDPOINTS.index}?${params.toString()}`;
}

function emptyPPessoaIndexResult(perPage = DEFAULT_PAGINATION_META.per_page): PPessoaIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executePPessoaIndexData(query?: PPessoaIndexQuery): Promise<PPessoaIndexResult> {
  const api = new API();
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPPessoaIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyPPessoaIndexResult(perPage);
  }

  const rows = Array.isArray(response?.data) ? (response.data as PPessoaInterface[]) : [];
  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const PPessoaIndexData = withClientErrorHandler(executePPessoaIndexData);
