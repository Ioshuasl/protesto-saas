import * as z from 'zod';

export const ocorrenciaAndamentoFormSchema = z.object({
  codigo: z
    .string()
    .min(1, 'Código é obrigatório')
    .max(10, 'Código deve ter no máximo 10 caracteres'),
  descricao: z.string().min(1, 'Descrição é obrigatória'),
});

export type OcorrenciaAndamentoFormValues = z.infer<typeof ocorrenciaAndamentoFormSchema>;
