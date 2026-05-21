import type { PBancoIndexQuery } from '@/packages/administrativo/interfaces/PBanco/PBancoIndexQuery';

export type PBancoFilterState = {
  search: string;
};

export const defaultPBancoFilterState: PBancoFilterState = {
  search: '',
};

export function buildPBancoIndexQuery(state: PBancoFilterState): PBancoIndexQuery | undefined {
  const busca = state.search.trim();
  if (!busca) return undefined;
  return { busca };
}
