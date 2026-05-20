export type PCertidaoTipoCertidao = "P" | "N";
export type PCertidaoStatus = "A" | "C";

export interface PCertidaoInterface {
  certidao_id: number;
  usuario_id?: number;
  data_certidao?: Date;
  valor_emolumento?: number;
  valor_taxa_judiciaria?: number;
  valor_fundesp?: number;
  valor_taxa_extra?: number;
  numero_impressao?: number;
  observacao?: string;
  valor_taxa_iss?: number;
  hora_certidao?: string;
  nome?: string;
  apresentante?: string;
  tipo_certidao?: PCertidaoTipoCertidao;
  cpfcnpj?: string;
  status?: PCertidaoStatus;
  nfse_id?: number;
  qtd_protestos?: number;
  qtd_cancelados?: number;
  qtd_sustado?: number;
  n_remessa?: number;
  tipo_remessa?: string;
  protecao_credito_id?: number;
}
