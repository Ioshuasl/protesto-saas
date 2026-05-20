/** Sim / Não conforme domínio da API (S = sim, N = não). */
export enum PBancoSimNao {
  Sim = "S",
  Nao = "N",
}

/**
 * Interface gerada para a tabela P_BANCO
 */
export interface PBancoInterface {
  banco_id: number;
  codigo_banco?: string;
  pessoa_id?: number;
  layout_id?: number;
  demais_despesas?: number;
  descricao?: string;
  apontamento_pag_posterior?: PBancoSimNao;
  custas_na_confirmacao?: PBancoSimNao;
}
