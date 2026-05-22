/**
 * Interface gerada para a tabela P_OCORRENCIA_ANDAMENTO
 */
export interface POcorrenciaAndamentoInterface {
  ocorrencia_andamento_id: number;
  codigo?: string;
  descricao?: string;
}

/** Payload de create/update antes do formulário dedicado. */
export type POcorrenciaAndamentoSavePayload = {
  codigo: string;
  descricao: string;
};
