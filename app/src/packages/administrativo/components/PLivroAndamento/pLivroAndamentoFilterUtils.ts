import type { PLivroAndamentoIndexQuery } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoIndexQuery';

export type PLivroAndamentoFilterState = {
  search: string;
};

export const defaultPLivroAndamentoFilterState: PLivroAndamentoFilterState = {
  search: '',
};

export function buildPLivroAndamentoIndexQuery(
  state: PLivroAndamentoFilterState,
): PLivroAndamentoIndexQuery | undefined {
  const busca = state.search.trim();
  if (!busca) return undefined;
  return { busca };
}
