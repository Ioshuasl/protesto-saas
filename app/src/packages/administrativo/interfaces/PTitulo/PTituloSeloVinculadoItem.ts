/**
 * Selo vinculado ao título (camada de apresentação / resposta de API enriquecida).
 */
export interface PTituloSeloVinculadoItem {
  /** Agrupador do selo. */
  selo_agrupador?: string;
  /** Identificador / série do selo. */
  sigla?: string;
  numero_selo?: string;
  numero?: number;
  /** Código do tipo de ato. */
  codigo_ato?: string | number;
  tipo_ato?: string | number;
  /** Rótulo curto do ato. */
  descricao?: string;
  descricao_ato?: string;
  /** Texto longo (tabela de emolumentos / serviço). */
  descricao_completa?: string;
  /** Nome do serventuário quando a API envia o texto. */
  nome_completo?: string;
  /** Usuário (serventuário) em G_USUARIO.usuario_id, se não houver nome completo. */
  usuario_id?: number;
  data_hora_utilizacao?: string | Date;
  /** Ex.: "02.02.2026 08:50". */
  data?: string;
  valor_emolumento?: number;
  valor_taxa_judiciaria?: number;
  valor_fundesp?: number;
  valor_total?: number;
  /** Identificador interno; não exibido na tela de listagem. */
  selo_livro_id?: number;
}
