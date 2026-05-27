import { mapIndexItemToTituloListItem } from '@/packages/administrativo/data/PTitulo/ptituloApiMappers';
import { buildPTituloIndexEndpoint } from '@/packages/administrativo/data/PTitulo/ptituloIndexQueryBuilder';
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

function emptyPTituloIndexResult(perPage = DEFAULT_PAGINATION_META.per_page): PTituloIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

export function createPTituloSomenteIndexData(baseEndpoint: string) {
  async function execute(query?: PTituloIndexQuery): Promise<PTituloIndexResult> {
    const api = new API();
    const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

    const response = await api.send({
      method: Methods.GET,
      endpoint: buildPTituloIndexEndpoint(baseEndpoint, query),
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

  return withClientErrorHandler(execute);
}
