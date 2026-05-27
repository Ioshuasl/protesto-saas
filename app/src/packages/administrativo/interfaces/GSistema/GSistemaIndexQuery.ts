export type GSistemaIndexQuery = {
  descricao?: string;
  situacao?: string;
  tipo_cartorio?: string;
  /** Página da API (query `p`). */
  page?: number;
  per_page?: number;
  sort?: string;
};
