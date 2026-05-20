/**
 * Interface gerada para a tabela P_CUSTAS_CANCELAMENTO
 */
export interface PCustasCancelamentoInterface {
  custas_cancelamento_id: number;
  faixa?: string;
  custas?: number;
  taxas?: number;
  valor_fixo?: number;
  iss?: number;
  valor_inicial?: number;
  valor_final?: number;
  emolumento_periodo_id?: number;
}
