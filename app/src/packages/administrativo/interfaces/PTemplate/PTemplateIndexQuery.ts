export type PTemplateIndexQuery = {
  template_id?: number;
  descricao?: string;
  /** Página da API (query `p`). */
  page?: number;
  per_page?: number;
  /** formato3: ex. template_id.desc */
  sort?: string;
};
