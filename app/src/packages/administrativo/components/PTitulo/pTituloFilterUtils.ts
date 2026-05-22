import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';

export type PTituloFilterState = {
  search: string;
  status: string;
  startDate: string;
  endDate: string;
};

export const defaultPTituloFilterState: PTituloFilterState = {
  search: '',
  status: 'all',
  startDate: '',
  endDate: '',
};

export function buildPTituloIndexQuery(
  state: PTituloFilterState,
  overrides?: Pick<PTituloIndexQuery, 'page' | 'per_page' | 'sort'>,
): PTituloIndexQuery {
  const query: PTituloIndexQuery = {
    sort: 'titulo_id.desc',
    ...overrides,
  };

  const search = state.search.trim();
  if (search) query.busca_pessoa = search;

  return query;
}
