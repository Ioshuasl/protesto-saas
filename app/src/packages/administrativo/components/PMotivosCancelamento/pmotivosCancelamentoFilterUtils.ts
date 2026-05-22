import type { PMotivosCancelamentoIndexQuery } from '@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoIndexQuery';

export type PMotivosCancelamentoFilterState = {
  search: string;
};

export const defaultPMotivosCancelamentoFilterState: PMotivosCancelamentoFilterState = {
  search: '',
};

export function buildPMotivosCancelamentoIndexQuery(
  state: PMotivosCancelamentoFilterState,
): PMotivosCancelamentoIndexQuery | undefined {
  const descricao = state.search.trim();
  if (!descricao) return undefined;
  return { descricao };
}
