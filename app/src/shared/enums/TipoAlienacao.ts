// TipoAlienacaoEnum.ts
export const TipoAlienacaoEnum = {
  1: 'Quitado à vista',
  2: 'Quitado à prazo',
  3: 'A prazo',
  4: 'Não se Aplica',
  5: 'Quitado sem informação da forma de pagamento',
} as const;

export type TipoAlienacaoKey = keyof typeof TipoAlienacaoEnum;
