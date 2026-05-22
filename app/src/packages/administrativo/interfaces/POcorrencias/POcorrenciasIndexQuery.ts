export type POcorrenciasIndexQuery = {
  /** LIKE em DESCRICAO ou CODIGO (query `busca`). */
  busca?: string;
  tipo?: string;
  page?: number;
  per_page?: number;
};
