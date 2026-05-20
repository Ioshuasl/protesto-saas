export const ConfirmacaoEnum = {
  S: 'Sim',
  N: 'Não',
} as const;

export type ConfirmacaoKey = keyof typeof ConfirmacaoEnum; // 'S' | 'N'
