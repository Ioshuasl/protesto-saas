/** Rotas em api/packages/v1/administrativo/endpoints/p_livro_andamento_endpoint.py */
export const PLIVRO_ANDAMENTO_ENDPOINTS = {
  index: 'administrativo/p_livro_andamento/',
  show: (id: number) => `administrativo/p_livro_andamento/${id}`,
  create: 'administrativo/p_livro_andamento/',
  update: (id: number) => `administrativo/p_livro_andamento/${id}`,
  finalizar: (id: number) => `administrativo/p_livro_andamento/finalizar/${id}`,
  delete: (id: number) => `administrativo/p_livro_andamento/${id}`,
  proximoNumeroLivro: (livroNaturezaId: number) =>
    `administrativo/p_livro_andamento/proximo-numero-livro/${livroNaturezaId}`,
};

/** Listagem ampla para selects (ex.: PTitulo). */
export const PLIVRO_ANDAMENTO_LIST_QUERY = {
  page: 1,
  per_page: 100,
  sort: 'data_abertura.desc',
} as const;
