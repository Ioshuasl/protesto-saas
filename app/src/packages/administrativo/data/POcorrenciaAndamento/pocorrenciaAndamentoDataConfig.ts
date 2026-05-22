import type { POcorrenciaAndamentoIndexQuery } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoIndexQuery';

/** Rotas em api/packages/v1/administrativo/endpoints/p_ocorrencia_andamento_endpoint.py */
export const POCORRENCIA_ANDAMENTO_ENDPOINTS = {
  index: 'administrativo/p_ocorrencia_andamento/',
  show: (id: number) => `administrativo/p_ocorrencia_andamento/${id}`,
  create: 'administrativo/p_ocorrencia_andamento/',
  update: (id: number) => `administrativo/p_ocorrencia_andamento/${id}`,
  delete: (id: number) => `administrativo/p_ocorrencia_andamento/${id}`,
};

/** Listagem ampla para selects e comboboxes. */
export const POCORRENCIA_ANDAMENTO_LIST_QUERY: POcorrenciaAndamentoIndexQuery = {
  page: 1,
  per_page: 500,
  sort: 'ocorrencia_andamento_id.asc',
};
