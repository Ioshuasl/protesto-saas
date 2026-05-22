import type { PMotivosIndexQuery } from '@/packages/administrativo/interfaces/PMotivos/PMotivosIndexQuery';

export const PMOTIVOS_FILTER_ALL = '__all__';

export type PMotivosFilterState = {
  search: string;
  situacao: string;
};

export const defaultPMotivosFilterState: PMotivosFilterState = {
  search: '',
  situacao: PMOTIVOS_FILTER_ALL,
};

export function buildPMotivosIndexQuery(state: PMotivosFilterState): PMotivosIndexQuery | undefined {
  const params: PMotivosIndexQuery = {};

  if (state.situacao && state.situacao !== PMOTIVOS_FILTER_ALL) {
    params.situacao = state.situacao;
  }

  return Object.keys(params).length > 0 ? params : undefined;
}
