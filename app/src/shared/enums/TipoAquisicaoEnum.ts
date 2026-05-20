export const TipoAquisicaoEnum = {
  1: 'Havido por Compra Feita Contrato',
  2: 'Havido por Compra Feita Normal',
  3: 'Havido por Desmembramento',
  4: 'Havido por Legitima Aquisição',
  5: 'Não possui tipo aquisição',
} as const;

export type TipoAquisicaoKey = keyof typeof TipoAquisicaoEnum; // "1" | "2" | ...
export type TipoAquisicaoValue = (typeof TipoAquisicaoEnum)[TipoAquisicaoKey]; // Retorna os valores em inteiros
