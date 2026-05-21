export type GFeriadoIndexQuery = {
  tipo?: string;
  situacao?: string;
  descricao?: string;
  ano?: number;
  /** Página da API (query `p`). */
  page?: number;
  per_page?: number;
};
