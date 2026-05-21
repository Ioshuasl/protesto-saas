import { z } from 'zod';

export const GUsuarioAuth2FAOTP_LENGTH = 6;

export const GUsuarioAuth2FALoginSchema = z.object({
  codigo_seguranca: z
    .string()
    .length(GUsuarioAuth2FAOTP_LENGTH, `Informe os ${GUsuarioAuth2FAOTP_LENGTH} dígitos do código`)
    .regex(/^\d+$/, 'Use apenas números'),
});

export type GUsuarioAuth2FALoginFormValues = z.infer<typeof GUsuarioAuth2FALoginSchema>;
