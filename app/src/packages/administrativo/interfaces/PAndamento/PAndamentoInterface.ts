import type { POcorrenciaAndamentoInterface } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface';

/** Siglas P_ANDAMENTO.ARQUIVO_GERADO — D = Aguardando; E = Exportado */
export type PAndamentoArquivoGeradoCodigo = 'D' | 'E';

/** Include de P_OCORRENCIA_ANDAMENTO no endpoint `/titulo/{titulo_id}`. */
export type PAndamentoOcorrenciaAndamentoEmbed = Pick<
  POcorrenciaAndamentoInterface,
  'ocorrencia_andamento_id' | 'codigo' | 'descricao'
>;

/**
 * Interface para a tabela P_ANDAMENTO (histórico de andamento do título).
 */
export interface PAndamentoInterface {
  andamento_id: number;
  ocorrencia_andamento_id?: number;
  data_ocorrencia?: string;
  titulo_id?: number;
  usuario_id?: number;
  arquivo_gerado?: PAndamentoArquivoGeradoCodigo | string;
  data_geracao?: string | null;
  ocorrencia_andamento?: PAndamentoOcorrenciaAndamentoEmbed | null;
}

export type PAndamentoSavePayload = {
  ocorrencia_andamento_id: number;
  data_ocorrencia: string;
  titulo_id: number;
  usuario_id: number;
  arquivo_gerado: PAndamentoArquivoGeradoCodigo;
  data_geracao?: string | null;
};

export type PAndamentoUpdatePayload = Partial<PAndamentoSavePayload>;
