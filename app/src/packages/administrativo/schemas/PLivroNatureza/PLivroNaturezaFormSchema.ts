import * as z from "zod";

export const livroNaturezaFormSchema = z.object({
  sigla: z.string().min(1, "Sigla é obrigatória"),
  descricao: z.string().min(1, "Descrição é obrigatória"),
  tipo: z.string().min(1, "Tipo é obrigatório"),
  situacao: z.string().min(1, "Situação é obrigatória"),
});

export type LivroNaturezaFormValues = z.infer<typeof livroNaturezaFormSchema>;
