export type PMotivosIndexQuery = {
  descricao?: string;
  situacao?: string;
  /** Página da API (query `p`). */
  page?: number;
  per_page?: number;
};
