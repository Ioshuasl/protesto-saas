import * as z from "zod";

export const feriadoFormSchema = z.object({
  data: z.date({
    message: "A data é obrigatória.",
  }),
  descricao: z.string().min(1, "Descrição é obrigatória"),
  tipo: z.string().min(1, "Tipo é obrigatório"),
  situacao: z.string().min(1, "Situação é obrigatória"),
});

export type FeriadoFormValues = z.infer<typeof feriadoFormSchema>;
