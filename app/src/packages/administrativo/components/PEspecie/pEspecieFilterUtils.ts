import type { PEspecieIndexQuery } from '@/packages/administrativo/interfaces/PEspecie/PEspecieIndexQuery';

export type PEspecieFilterState = {
  search: string;
};

export const defaultPEspecieFilterState: PEspecieFilterState = {
  search: '',
};

export function buildPEspecieIndexQuery(
  state: PEspecieFilterState,
): PEspecieIndexQuery | undefined {
  const busca = state.search.trim();
  if (!busca) return undefined;
  return { busca };
}
