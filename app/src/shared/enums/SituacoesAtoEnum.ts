export const SituacoesAtoEnum = {
  0: 'Doc. Pendente',
  1: 'Montagem',
  2: 'Pré-lavrado',
  3: 'Lavrado',
  4: 'Cancelado',
  6: 'Substabelecido',
  7: 'Revogado',
  8: 'Reratificado',
  9: 'Renunciado',
  10: 'Renúncia',
  11: 'Renúncia Parcial',
} as const;

export type SituacoesAtoValue = keyof typeof SituacoesAtoEnum;
