import { z } from 'zod';

export const GUsuarioLoginSchema = z.object({
  identificador: z
    .string()
    .min(1, 'Informe login, e-mail ou CPF'),
  senha_api: z.string().min(1, 'O campo deve ser preenchido'),
});

export type GUsuarioLoginFormValues = z.infer<typeof GUsuarioLoginSchema>;
