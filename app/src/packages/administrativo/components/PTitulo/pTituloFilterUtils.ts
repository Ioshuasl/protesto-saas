import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';

export type PTituloFilterState = {
  search: string;
  startDate: string;
  endDate: string;
  bancoId: string;
  especieId: string;
  ocorrenciaId: string;
};

export const defaultPTituloFilterState: PTituloFilterState = {
  search: '',
  startDate: '',
  endDate: '',
  bancoId: '',
  especieId: '',
  ocorrenciaId: '',
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
  if (search) query.busca = search;

  const bancoId = Number(state.bancoId);
  if (Number.isFinite(bancoId) && bancoId > 0) query.banco_id = bancoId;

  const especieId = Number(state.especieId);
  if (Number.isFinite(especieId) && especieId > 0) query.especie_id = especieId;

  const ocorrenciaId = Number(state.ocorrenciaId);
  if (Number.isFinite(ocorrenciaId) && ocorrenciaId > 0) query.ocorrencia_id = ocorrenciaId;

  return query;
}
