export enum SituacoesEnum {
  A = 'Ativo',
  I = 'Inativo',
}

// Exporta os valroes da chave
export type SituacaoKey = keyof typeof SituacoesEnum;
