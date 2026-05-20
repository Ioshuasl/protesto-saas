/**
 * Interface gerada para a tabela P_ARQUIVO_TITULO
 */
export interface PArquivoTituloInterface {
  arquivo_titulo_id: number;
  data_importacao?: Date;
  quantidade?: number;
  data_movimento?: string;
  numero_sequencial?: string;
  qtde_registros?: string;
  qtde_titulos?: string;
  qtde_indicacoes?: string;
  qtde_originais?: string;
  soma_vlr_remessa?: number;
  soma_qtde_remessa?: number;
  texto?: string;
  agencia_centralizadora?: string;
  codigo_praca?: string;
  sequencial_header?: string;
  nome_arquivo?: string;
  portador_nome?: string;
  complemento_header?: string;
  complemento_registro?: string;
  identificacao_registro?: string;
  portador_codigo?: string;
  id_transacao_remetente?: string;
  id_transacao_destinatario?: string;
  id_transacao_tipo?: string;
  versao_layout?: string;
  sequencial_footer?: string;
  texto_importado?: string;
}
