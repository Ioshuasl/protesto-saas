export const TipoDeAssinaturaEnum = {
  1: 'Assinatura normal',
  2: 'Assinatura pela digital',
  3: 'Não assina (Faz parte do ato)',
  4: 'Não assina(Somente qualifica)',
  5: 'Assinatura Digital E - Notariado',
} as const;

export type TipoDeAssinaturaKey = keyof typeof TipoDeAssinaturaEnum;
