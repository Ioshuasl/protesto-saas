export const TipoCertidoesEnum = {
  1: 'Sistema',
  2: 'Imagem',
  3: 'Imagem Antiga',
  4: 'Transcrever',
  5: 'Negativa/Positiva',
} as const;

export type TipoCertidaoEnum = keyof typeof TipoCertidoesEnum;
