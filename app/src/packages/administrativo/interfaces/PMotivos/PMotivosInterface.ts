/**
 * Interface gerada para a tabela P_MOTIVOS
 */
export interface PMotivosInterface {
  motivos_id: number;
  descricao?: string;
  situacao?: string;
  codigo?: string;
  /** Presente na listagem (index): quantidade de títulos com MOTIVO_APONTAMENTO_ID. */
  total_titulos?: number;
}
