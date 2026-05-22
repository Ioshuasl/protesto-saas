import type { POcorrenciasIndexQuery } from '@/packages/administrativo/interfaces/POcorrencias/POcorrenciasIndexQuery';

export const POCORRENCIAS_FILTER_ALL = '__all__';

export type POcorrenciasFilterState = {
  search: string;
  tipo: string;
};

export const defaultPOcorrenciasFilterState: POcorrenciasFilterState = {
  search: '',
  tipo: POCORRENCIAS_FILTER_ALL,
};

export function buildPOcorrenciasIndexQuery(
  state: POcorrenciasFilterState,
): POcorrenciasIndexQuery | undefined {
  const params: POcorrenciasIndexQuery = {};

  if (state.search.trim()) {
    params.busca = state.search.trim();
  }
  if (state.tipo && state.tipo !== POCORRENCIAS_FILTER_ALL) {
    params.tipo = state.tipo;
  }

  return Object.keys(params).length > 0 ? params : undefined;
}
