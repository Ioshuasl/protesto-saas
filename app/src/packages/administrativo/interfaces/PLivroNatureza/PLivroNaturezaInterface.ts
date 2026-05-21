import type { SituacaoKey } from '@/shared/enums/SituacoesEnum';

/**
 * Contrato API P_LIVRO_NATUREZA (tipo e natureza_id omitidos na API).
 */
export interface PLivroNaturezaInterface {
  livro_natureza_id: number;
  descricao?: string;
  /** Siglas da API: A = ativo, I = inativo */
  situacao?: SituacaoKey | string;
  sigla?: string;
}
