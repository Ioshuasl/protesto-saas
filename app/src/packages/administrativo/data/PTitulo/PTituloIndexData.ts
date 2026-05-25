'use server';

import { mapIndexItemToTituloListItem } from '@/packages/administrativo/data/PTitulo/ptituloApiMappers';
import { PTITULO_ENDPOINTS } from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import type { PTituloIndexItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexItem';
import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import type { PTituloIndexResult } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexResult';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from '@/shared/components/pagination';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildPTituloIndexEndpoint(query?: PTituloIndexQuery): string {
  const params = new URLSearchParams();

  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set('p', String(page));
  params.set('per_page', String(perPage));
  params.set('sort', query?.sort ?? 'titulo_id.desc');

  if (query?.busca) params.set('busca', query.busca);
  if (query?.busca_pessoa) params.set('busca_pessoa', query.busca_pessoa);
  if (query?.numero_apontamento != null) params.set('numero_apontamento', String(query.numero_apontamento));
  if (query?.nosso_numero) params.set('nosso_numero', query.nosso_numero);
  if (query?.numero_titulo) params.set('numero_titulo', query.numero_titulo);
  if (query?.numero_titulo_banco) params.set('numero_titulo_banco', query.numero_titulo_banco);
  if (query?.ocorrencia_id != null) params.set('ocorrencia_id', String(query.ocorrencia_id));
  if (query?.ocorrencia_andamento_id != null) {
    params.set('ocorrencia_andamento_id', String(query.ocorrencia_andamento_id));
  }
  if (query?.banco_id != null) params.set('banco_id', String(query.banco_id));
  if (query?.especie_id != null) params.set('especie_id', String(query.especie_id));

  const qs = params.toString();
  return qs ? `${PTITULO_ENDPOINTS.index}?${qs}` : PTITULO_ENDPOINTS.index;
}

function emptyPTituloIndexResult(perPage = DEFAULT_PAGINATION_META.per_page): PTituloIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executePTituloIndexData(query?: PTituloIndexQuery): Promise<PTituloIndexResult> {
  const api = new API();
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPTituloIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyPTituloIndexResult(perPage);
  }

  const rawRows = Array.isArray(response?.data) ? (response.data as PTituloIndexItem[]) : [];
  const rows = rawRows
    .filter((row) => row?.titulo_id != null)
    .map((row) => mapIndexItemToTituloListItem(row));

  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const PTituloIndexData = withClientErrorHandler(executePTituloIndexData);
