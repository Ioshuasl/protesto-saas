/** Rotas em api/packages/v1/administrativo/endpoints/p_livro_natureza_endpoint.py */
export const PLIVRO_NATUREZA_ENDPOINTS = {
  index: 'administrativo/p_livro_natureza/',
  show: (id: number) => `administrativo/p_livro_natureza/${id}`,
  create: 'administrativo/p_livro_natureza/',
  update: (id: number) => `administrativo/p_livro_natureza/${id}`,
  delete: (id: number) => `administrativo/p_livro_natureza/${id}`,
};

/** Listagem ampla para selects (ex.: PLivroAndamento). */
export const PLIVRO_NATUREZA_LIST_QUERY = {
  page: 1,
  per_page: 100,
  sort: 'livro_natureza_id.asc',
} as const;
