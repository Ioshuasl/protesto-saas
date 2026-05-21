export type PLivroNaturezaIndexQuery = {
  /** Busca unificada em SIGLA ou DESCRICAO (OR). */
  busca?: string;
  page?: number;
  per_page?: number;
  sort?: string;
};
