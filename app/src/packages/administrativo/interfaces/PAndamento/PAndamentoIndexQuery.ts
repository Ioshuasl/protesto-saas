export type PAndamentoIndexQuery = {
  titulo_id?: number;
  ocorrencia_andamento_id?: number;
  /** ISO date ou datetime — filtro enviado como query `data_ocorrencia`. */
  data_ocorrencia?: string;
  /** Página da API (query `p`). */
  page?: number;
  per_page?: number;
  sort?: string;
};
