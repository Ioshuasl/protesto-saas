import type { PLivroNaturezaIndexQuery } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaIndexQuery';

export type PLivroNaturezaFilterState = {
  search: string;
};

export const defaultPLivroNaturezaFilterState: PLivroNaturezaFilterState = {
  search: '',
};

export function buildPLivroNaturezaIndexQuery(
  state: PLivroNaturezaFilterState,
): PLivroNaturezaIndexQuery | undefined {
  const busca = state.search.trim();
  if (!busca) return undefined;
  return { busca };
}
