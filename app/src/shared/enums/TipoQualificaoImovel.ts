// TipoQualificaoImovelEnum.ts
export const TipoQualificaoImovelEnum = {
  1: 'Conjugue Compra',
  2: 'Imóvel Geral (Diversas Unidades)',
  3: 'Imóvel Individual',
  4: 'Já Qualificado',
  5: 'Não Qualificar',
  6: 'Nome Tipo',
} as const;

export type TipoQualificaoImovelKey = keyof typeof TipoQualificaoImovelEnum;
