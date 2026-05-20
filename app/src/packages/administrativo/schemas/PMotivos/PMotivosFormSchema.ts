import * as z from "zod";

export const motivoFormSchema = z.object({
  codigo: z.string().min(1, "Código é obrigatório"),
  descricao: z.string().min(1, "Descrição é obrigatória"),
  situacao: z.string().min(1, "Situação é obrigatória"),
});

export type MotivoFormValues = z.infer<typeof motivoFormSchema>;
