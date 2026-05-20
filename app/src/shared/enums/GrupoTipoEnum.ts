export const GrupoTipoEnum = {
  V: 'Variável',
  Q: 'Qualificação',
  M: 'Minuta',
} as const;

export type GrupoTipoKey = keyof typeof GrupoTipoEnum;
