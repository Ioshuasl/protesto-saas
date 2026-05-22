import type { POcorrenciaAndamentoIndexQuery } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoIndexQuery';

export type POcorrenciaAndamentoFilterState = {
  search: string;
};

export const defaultPOcorrenciaAndamentoFilterState: POcorrenciaAndamentoFilterState = {
  search: '',
};

export function buildPOcorrenciaAndamentoIndexQuery(
  state: POcorrenciaAndamentoFilterState,
): POcorrenciaAndamentoIndexQuery | undefined {
  const descricao = state.search.trim();
  if (!descricao) return undefined;
  return { descricao };
}
