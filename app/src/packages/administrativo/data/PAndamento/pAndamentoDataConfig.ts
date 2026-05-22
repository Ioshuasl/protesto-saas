import type { PAndamentoIndexQuery } from '@/packages/administrativo/interfaces/PAndamento/PAndamentoIndexQuery';

/** Rotas em api/packages/v1/administrativo/endpoints/p_andamento_endpoint.py */
export const PANDAMENTO_ENDPOINTS = {
  index: 'administrativo/p_andamento/',
  /** Andamentos do título com `ocorrencia_andamento` (include ORM). */
  indexByTitulo: (tituloId: number) => `administrativo/p_andamento/titulo/${tituloId}`,
  show: (id: number) => `administrativo/p_andamento/${id}`,
  create: 'administrativo/p_andamento/',
  update: (id: number) => `administrativo/p_andamento/${id}`,
  delete: (id: number) => `administrativo/p_andamento/${id}`,
};

/** Query para `PAndamentoIndexByTituloData` / `getAllByTitulo` (titulo_id no path). */
export function buildPAndamentoListQueryByTitulo(
  overrides?: Omit<PAndamentoIndexQuery, 'titulo_id'>,
): Omit<PAndamentoIndexQuery, 'titulo_id'> {
  return {
    page: 1,
    per_page: 100,
    sort: 'andamento_id.desc',
    ...overrides,
  };
}
