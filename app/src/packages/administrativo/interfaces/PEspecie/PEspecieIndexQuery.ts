export type PEspecieIndexQuery = {
  /** Busca unificada em ESPECIE ou DESCRICAO (OR). */
  busca?: string;
  /** Página da API (query `p`). */
  page?: number;
  per_page?: number;
  /** formato3: ex. especie_id.desc */
  sort?: string;
};
