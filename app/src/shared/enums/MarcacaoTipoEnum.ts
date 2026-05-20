export const MarcacaoTipoEnum = {
  L: 'Lista',
  T: 'Texto',
} as const;

export type MarcacaoTipoKey = keyof typeof MarcacaoTipoEnum;
