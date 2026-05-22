/**
 * Interface gerada para a tabela P_OCORRENCIAS
 */
export interface POcorrenciasInterface {
  ocorrencias_id: number;
  tipo?: string;
  codigo?: string;
  descricao?: string;
  /** Preenchido no index da API quando há vínculo em P_TITULO. */
  total_titulos?: number;
}
