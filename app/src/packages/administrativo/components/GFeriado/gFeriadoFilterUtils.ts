import type { GFeriadoIndexQuery } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoIndexQuery';

export const GFERIADO_FILTER_ALL = '__all__';

export type GFeriadoFilterState = {
  search: string;
  tipo: string;
  situacao: string;
};

export const defaultGFeriadoFilterState: GFeriadoFilterState = {
  search: '',
  tipo: GFERIADO_FILTER_ALL,
  situacao: GFERIADO_FILTER_ALL,
};

export function buildGFeriadoIndexQuery(state: GFeriadoFilterState): GFeriadoIndexQuery | undefined {
  const params: GFeriadoIndexQuery = {};

  if (state.tipo && state.tipo !== GFERIADO_FILTER_ALL) {
    params.tipo = state.tipo;
  }
  if (state.situacao && state.situacao !== GFERIADO_FILTER_ALL) {
    params.situacao = state.situacao;
  }

  return Object.keys(params).length > 0 ? params : undefined;
}
