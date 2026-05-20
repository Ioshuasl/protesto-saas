/**
 * Interface gerada para a tabela P_LIVRO_ANDAMENTO
 */
export interface PLivroAndamentoInterface {
  livro_andamento_id: number;
  livro_natureza_id?: number;
  folha_atual?: number;
  numero_livro?: number;
  data_abertura?: Date;
  data_fechamento?: Date;
  numero_folhas?: number;
  usuario_id?: number;
  numero_livro_letra?: string;
  sigla?: string;
}
