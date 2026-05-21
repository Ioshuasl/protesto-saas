export type PBancoIndexQuery = {
  /** Busca unificada em CODIGO_BANCO ou DESCRICAO (OR). */
  busca?: string;
  /** Página da API (query `p`). */
  page?: number;
  per_page?: number;
  /** formato3: ex. banco_id.desc */
  sort?: string;
};
