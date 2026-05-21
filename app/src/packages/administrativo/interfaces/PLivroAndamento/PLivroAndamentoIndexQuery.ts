export type PLivroAndamentoIndexQuery = {
  /** Busca unificada: SIGLA (LIKE) ou NUMERO_LIVRO (exato). */
  busca?: string;
  livro_natureza_id?: number;
  /** S = aberto (DATA_FECHAMENTO null); N = fechado */
  aberto?: 'S' | 'N';
  page?: number;
  per_page?: number;
  sort?: string;
};
